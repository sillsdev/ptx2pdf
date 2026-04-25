import logging
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango

from .sectionBase import SectionPanel, makeVBox, makeHBox, makeButton, makeSectionTitle, GLib_escape

logger = logging.getLogger(__name__)


class RecipeSection(SectionPanel):
    sectionId = "recipe"

    def _buildUi(self):
        self.pack_start(makeSectionTitle("Choose a Starting Point"), False, False, 0)

        intro = Gtk.Label(label=(
            "Select a recipe to pre-fill common settings, or start from scratch. "
            "You can change any setting afterwards."
        ))
        intro.set_xalign(0.0)
        intro.set_line_wrap(True)
        intro.show()
        self.pack_start(intro, False, False, 0)

        # Resume row (shown only when saved state exists)
        self._resumeBox = makeHBox(spacing=8)
        resumeIcon = Gtk.Label(label="↩")
        resumeIcon.show()
        resumeLabel = Gtk.Label(label="Resume previous setup")
        resumeLabel.set_xalign(0.0)
        resumeLabel.set_hexpand(True)
        resumeLabel.show()
        self._resumeBtn = Gtk.Button(label="Resume")
        self._resumeBtn.set_valign(Gtk.Align.CENTER)
        self._resumeBtn.show()
        self._resumeBox.pack_start(resumeIcon, False, False, 0)
        self._resumeBox.pack_start(resumeLabel, True, True, 0)
        self._resumeBox.pack_start(self._resumeBtn, False, False, 0)
        self._resumeBox.show()
        self._resumeBox.set_no_show_all(True)
        self.pack_start(self._resumeBox, False, False, 0)

        sep = Gtk.Separator()
        sep.show()
        self.pack_start(sep, False, False, 4)

        # Recipe cards list
        self._cardsBox = makeVBox(spacing=6)
        self._cardsBox.show()

        sw = Gtk.ScrolledWindow()
        sw.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        sw.set_min_content_height(300)
        sw.set_hexpand(True)
        sw.add(self._cardsBox)
        sw.show()
        self.pack_start(sw, True, True, 0)

        # Bottom options
        bottomBox = makeHBox(spacing=12)
        scratchBtn = Gtk.Button(label="Start from scratch")
        scratchBtn.set_valign(Gtk.Align.CENTER)
        scratchBtn.connect("clicked", self._onStartFromScratch)
        scratchBtn.show()

        self._resetBtn = Gtk.Button(label="Reset wizard")
        self._resetBtn.set_valign(Gtk.Align.CENTER)
        self._resetBtn.connect("clicked", self._onReset)
        self._resetBtn.show()

        self._dontAutoLaunchCheck = Gtk.CheckButton(label="Don't auto-launch the wizard for new projects")
        self._dontAutoLaunchCheck.show()

        bottomBox.pack_start(scratchBtn, False, False, 0)
        bottomBox.pack_start(self._resetBtn, False, False, 0)
        bottomBox.pack_end(self._dontAutoLaunchCheck, False, False, 0)
        bottomBox.show()

        sep2 = Gtk.Separator()
        sep2.show()
        self.pack_start(sep2, False, False, 4)
        self.pack_start(bottomBox, False, False, 0)

        self._selectedRecipeId = None
        self._recipeCards = {}

    def populateRecipes(self, recipes, savedStateExists=False):
        """Called by controller with recipe list from RecipeLoader."""
        for child in list(self._cardsBox.get_children()):
            self._cardsBox.remove(child)
        self._recipeCards.clear()

        self._resumeBox.set_visible(savedStateExists)

        for recipe in recipes:
            card = self._makeRecipeCard(recipe)
            self._cardsBox.pack_start(card, False, False, 0)

    def _makeRecipeCard(self, recipe):
        recipeId = recipe.get("id", "")
        label = recipe.get("label", recipeId)
        desc = recipe.get("description", "")
        tags = recipe.get("tags", [])

        frame = Gtk.Frame()
        frame.set_shadow_type(Gtk.ShadowType.ETCHED_IN)

        inner = makeVBox(spacing=4)
        inner.set_margin_start(8)
        inner.set_margin_end(8)
        inner.set_margin_top(6)
        inner.set_margin_bottom(6)

        titleRow = makeHBox(spacing=8)
        titleLbl = Gtk.Label()
        titleLbl.set_markup(f"<b>{GLib_escape(label)}</b>")
        titleLbl.set_xalign(0.0)
        titleLbl.set_hexpand(True)
        titleLbl.show()

        selectBtn = Gtk.Button(label="Select")
        selectBtn.set_valign(Gtk.Align.CENTER)
        selectBtn.connect("clicked", self._onSelectRecipe, recipeId)
        selectBtn.show()

        titleRow.pack_start(titleLbl, True, True, 0)
        titleRow.pack_start(selectBtn, False, False, 0)
        titleRow.show()

        descLbl = Gtk.Label(label=desc)
        descLbl.set_xalign(0.0)
        descLbl.set_line_wrap(True)
        descLbl.get_style_context().add_class("dim-label")
        descLbl.show()

        tagStr = "  ".join(f"#{t}" for t in tags)
        tagLbl = Gtk.Label(label=tagStr)
        tagLbl.set_xalign(0.0)
        tagLbl.get_style_context().add_class("dim-label")
        tagLbl.show()

        inner.pack_start(titleRow, False, False, 0)
        inner.pack_start(descLbl, False, False, 0)
        if tags:
            inner.pack_start(tagLbl, False, False, 0)
        inner.show()

        frame.add(inner)
        frame.show()

        self._recipeCards[recipeId] = frame
        return frame

    def _onSelectRecipe(self, _btn, recipeId):
        self._selectedRecipeId = recipeId
        self._emitStateChanged()

    def _onStartFromScratch(self, _btn):
        self._selectedRecipeId = None
        self._emitStateChanged()

    def _onReset(self, _btn):
        if self._onResetCb:
            self._onResetCb()

    def setResumeCallback(self, cb):
        self._resumeBtn.connect("clicked", lambda _b: cb())

    def setResetCallback(self, cb):
        self._onResetCb = cb

    def getSelectedRecipeId(self):
        return self._selectedRecipeId

    def getDontAutoLaunch(self):
        return self._dontAutoLaunchCheck.get_active()

    def setDontAutoLaunch(self, value):
        self._dontAutoLaunchCheck.set_active(value)

    def loadFromState(self, state):
        self._loading = True
        self._selectedRecipeId = state.recipeId
        self._loading = False

    def saveToState(self, state):
        state.recipeId = self._selectedRecipeId

    def isComplete(self):
        return True  # recipe selection is always optional
