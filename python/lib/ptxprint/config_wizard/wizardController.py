import json
import logging
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

from .wizardState import WizardState, SectionStatus
from .constraintsEngine import ConstraintsEngine
from .costEstimator import CostEstimator
from .pageCountEstimator import PageCountEstimator
from .recipeLoader import RecipeLoader
from .settingsMapper import SettingsMapper
from .sections import (RecipeSection, AudienceSection, ProductionSection,
                        TrimBindingSection, ContentSection, PeripheralsSection,
                        LayoutSection, ReviewSection)

logger = logging.getLogger(__name__)

SECTION_ORDER = [
    "recipe", "audience", "production", "trimBinding",
    "content", "peripherals", "layout", "review",
]


class WizardController:
    """
    Glues WizardState, ConstraintsEngine, estimators, and section panels together.
    Created by WizardWindow; does not own any top-level GTK window.
    """

    def __init__(self, dataDir: Path, statePath: Optional[Path] = None):
        self._dataDir   = dataDir
        self._statePath = statePath

        self._state   = WizardState()
        self._engine  = ConstraintsEngine(dataDir)
        self._costs   = CostEstimator(dataDir)
        self._pages   = PageCountEstimator()
        self._recipes = RecipeLoader(dataDir)
        self._mapper  = SettingsMapper()

        self._peripheralCatalogue: List[Dict] = []
        self._loadPeripheralCatalogue()

        self._sections: Dict[str, Any] = {}  # sectionId -> SectionPanel
        self._activeSection: str = "recipe"
        self._saveDebounceId: Optional[int] = None

        # Callbacks set by WizardWindow
        self._onSectionSwitchedCb: Optional[Callable] = None
        self._onFeedbackUpdatedCb: Optional[Callable] = None
        self._onSidebarUpdatedCb:  Optional[Callable] = None
        self._recomputing: bool = False

    def _loadPeripheralCatalogue(self):
        catPath = self._dataDir / "peripheralsCatalogue.json"
        try:
            with open(catPath, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._peripheralCatalogue = data.get("categories", [])
        except Exception as e:
            logger.error(f"Failed to load peripheralsCatalogue: {e}")

    # ── Section registration ───────────────────────────────────────────────

    def registerSection(self, sectionId: str, panel):
        self._sections[sectionId] = panel
        panel.setStateChangedCallback(self._onSectionStateChanged)

    def createSections(self) -> Dict[str, Any]:
        """Create all section panels and register them. Returns {sectionId: panel}."""
        recipe = RecipeSection()
        recipe.populateRecipes(self._recipes.allRecipes(),
                               savedStateExists=self._hasSavedState())
        recipe.setResumeCallback(self._onResume)
        recipe.setResetCallback(self._onReset)

        audience    = AudienceSection()
        production  = ProductionSection()
        trimBinding = TrimBindingSection()
        content     = ContentSection()
        peripherals = PeripheralsSection()
        peripherals.loadCatalogue(self._peripheralCatalogue)

        layout = LayoutSection()
        review = ReviewSection(jumpCallback=self.jumpToSection)

        panels = {
            "recipe":      recipe,
            "audience":    audience,
            "production":  production,
            "trimBinding": trimBinding,
            "content":     content,
            "peripherals": peripherals,
            "layout":      layout,
            "review":      review,
        }

        for sectionId, panel in panels.items():
            self.registerSection(sectionId, panel)

        return panels

    # ── Navigation ─────────────────────────────────────────────────────────

    def goNext(self):
        idx = SECTION_ORDER.index(self._activeSection)
        if idx < len(SECTION_ORDER) - 1:
            self.jumpToSection(SECTION_ORDER[idx + 1])

    def goBack(self):
        idx = SECTION_ORDER.index(self._activeSection)
        if idx > 0:
            self.jumpToSection(SECTION_ORDER[idx - 1])

    def jumpToSection(self, sectionId: str):
        self._saveCurrentSection()
        self._activeSection = sectionId
        panel = self._sections.get(sectionId)
        if panel:
            panel.loadFromState(self._state)
            # extra refresh for layout section (needs trim size)
            if sectionId == "layout" and hasattr(panel, "updateTrimSize"):
                panel.updateTrimSize(self._state.trimBinding.trimSize)
            # refresh review
            if sectionId == "review":
                self._refreshReview()
        if self._onSectionSwitchedCb:
            self._onSectionSwitchedCb(sectionId, panel)
        self._updateSidebar()

    def _saveCurrentSection(self):
        panel = self._sections.get(self._activeSection)
        if panel:
            panel.saveToState(self._state)

    # ── State change handling ──────────────────────────────────────────────

    def _onSectionStateChanged(self, sectionId: str):
        panel = self._sections.get(sectionId)
        if panel:
            panel.saveToState(self._state)

        self._recomputeAll()
        self._scheduleSave()

    def _recomputeAll(self):
        if self._recomputing:
            return
        self._recomputing = True
        try:
            self._doRecomputeAll()
        finally:
            self._recomputing = False

    def _doRecomputeAll(self):
        flat = self._state.getFlat()
        pageCount = self._pages.estimate(self._state, self._peripheralCatalogue)
        spineWidth = self._pages.spineWidthMm(pageCount, self._state.trimBinding.paperType)
        violations = self._engine.evaluateRules(flat, pageCount)
        perCopy, total = self._costs.estimate(flat)

        # Update sidebar status badges
        self._updateSectionStatuses(flat, violations)

        # Notify constraints change to all sections
        for panel in self._sections.values():
            panel.onConstraintsChanged(self._engine, flat)

        # Keep layout section trim-size-aware
        layoutPanel = self._sections.get("layout")
        if layoutPanel and hasattr(layoutPanel, "updateTrimSize"):
            layoutPanel.updateTrimSize(self._state.trimBinding.trimSize)

        # Notify feedback panel
        if self._onFeedbackUpdatedCb:
            self._onFeedbackUpdatedCb(
                pageCount, spineWidth, perCopy, total, violations,
                self._state.layout.columns or 1,
                self._state.trimBinding.trimSize or "a5",
            )

        # Recipe section: if a recipe was selected, apply it
        recipePanel = self._sections.get("recipe")
        if recipePanel:
            newRecipeId = recipePanel.getSelectedRecipeId()
            if newRecipeId and newRecipeId != self._state.recipeId:
                self._recipes.applyRecipe(newRecipeId, self._state)
                self._state.recipeId = newRecipeId
                # reload all panels from updated state
                for sid, panel in self._sections.items():
                    if sid != "recipe":
                        panel.loadFromState(self._state)
                self._recomputeAll()
                return

    def _updateSectionStatuses(self, flat, violations):
        for sectionId in SECTION_ORDER:
            prevStatus = SectionStatus(self._state.sectionStatus.get(sectionId, SectionStatus.notStarted))
            depChanged = self._isDependencyChanged(sectionId)
            status = self._engine.sectionStatus(sectionId, flat, violations, prevStatus, depChanged)
            self._state.sectionStatus[sectionId] = status
            if self._onSidebarUpdatedCb:
                self._onSidebarUpdatedCb(sectionId, status)

    def _isDependencyChanged(self, sectionId: str) -> bool:
        deps = self._engine.dependsOn(sectionId)
        if not deps:
            return False
        # Simplified: mark stale if section isn't yet complete and has deps
        for dep in deps:
            depStatus = self._state.sectionStatus.get(dep, SectionStatus.notStarted)
            if depStatus in (SectionStatus.complete, SectionStatus.hasWarnings):
                return True
        return False

    def _updateSidebar(self):
        idx = SECTION_ORDER.index(self._activeSection)
        if self._onSidebarUpdatedCb:
            pass  # individual status updates happen via _updateSectionStatuses
        isLast = (idx == len(SECTION_ORDER) - 1)
        if self._onSectionSwitchedCb:
            pass  # WizardWindow handles Back/Next button labels from activeSection

    # ── Recipe events ──────────────────────────────────────────────────────

    def _onResume(self):
        if self._statePath and self._statePath.exists():
            loaded = WizardState.loadFromFile(str(self._statePath))
            if loaded:
                self._state = loaded
                for sid, panel in self._sections.items():
                    panel.loadFromState(self._state)
                self._recomputeAll()

    def _onReset(self):
        self._state = WizardState()
        if self._statePath and self._statePath.exists():
            try:
                self._statePath.unlink()
            except Exception:
                pass
        for sid, panel in self._sections.items():
            panel.loadFromState(self._state)
        self._recomputeAll()

    def _hasSavedState(self) -> bool:
        return bool(self._statePath and self._statePath.exists())

    # ── Review section ─────────────────────────────────────────────────────

    def _refreshReview(self):
        reviewPanel = self._sections.get("review")
        if not reviewPanel:
            return
        flat = self._state.getFlat()
        pageCount = self._pages.estimate(self._state, self._peripheralCatalogue)
        spineWidth = self._pages.spineWidthMm(pageCount, self._state.trimBinding.paperType)
        violations = self._engine.evaluateRules(flat, pageCount)
        perCopy, total = self._costs.estimate(flat)
        reviewPanel.refresh(self._state, pageCount, spineWidth, perCopy, total, violations)

    # ── Apply actions ──────────────────────────────────────────────────────

    def applyToNewConfig(self, configName: str) -> bool:
        """
        Create a new named PTXprint configuration with wizard settings.
        TODO(integrate): call PTXprint's createConfig(configName, settings).
        """
        settings = self._mapper.mapAll(self._state)
        logger.info(f"Would create config '{configName}' with {len(settings)} settings")
        # TODO(integrate): ptxprint_view.createConfig(configName, settings)
        return True

    def applyToCurrentConfig(self, currentConfig: Dict[str, Any]) -> List:
        """
        Compute diff against currentConfig.
        TODO(integrate): call PTXprint's applyConfigDiff(configName, diffDict).
        """
        newSettings = self._mapper.mapAll(self._state)
        return self._mapper.computeDiff(currentConfig, newSettings)

    def getState(self) -> WizardState:
        return self._state

    def getMappedSettings(self) -> Dict[str, Any]:
        return self._mapper.mapAll(self._state)

    # ── Persistence ────────────────────────────────────────────────────────

    def _scheduleSave(self):
        if self._saveDebounceId is not None:
            GLib.source_remove(self._saveDebounceId)
        self._saveDebounceId = GLib.timeout_add(500, self._doSave)

    def _doSave(self):
        self._saveDebounceId = None
        if self._statePath:
            self._state.saveToFile(str(self._statePath))
        return False  # don't repeat

    def saveNow(self):
        if self._statePath:
            self._state.saveToFile(str(self._statePath))

    # ── Callback setters ───────────────────────────────────────────────────

    def setOnSectionSwitched(self, cb):
        self._onSectionSwitchedCb = cb

    def setOnFeedbackUpdated(self, cb):
        self._onFeedbackUpdatedCb = cb

    def setOnSidebarUpdated(self, cb):
        self._onSidebarUpdatedCb = cb

    @property
    def activeSection(self):
        return self._activeSection

    @property
    def sectionOrder(self):
        return SECTION_ORDER
