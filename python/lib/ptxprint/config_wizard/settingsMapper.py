import logging
from typing import Any, Dict, List, Optional, Tuple

from .wizardState import WizardState

logger = logging.getLogger(__name__)


class SettingsMapper:
    """
    Translates WizardState into PTXprint configuration key/value pairs.
    All mapping keys are marked TODO(integrate) for maintainer to fill in.
    """

    def mapAll(self, state: WizardState) -> Dict[str, Any]:
        result = {}
        result.update(self._mapTrim(state))
        result.update(self._mapLayout(state))
        result.update(self._mapContent(state))
        result.update(self._mapPeripherals(state))
        return result

    def _mapTrim(self, s: WizardState) -> Dict[str, Any]:
        result = {}
        if s.trimBinding.trimSize is not None:
            # TODO(integrate): map trimSize -> PTXprint paper size key
            result["TODO_paperSize"] = s.trimBinding.trimSize
        if s.trimBinding.paperType is not None:
            # TODO(integrate): map paperType -> PTXprint paper colour/weight key
            result["TODO_paperType"] = s.trimBinding.paperType
        if s.trimBinding.bindingType is not None:
            # TODO(integrate): map bindingType -> PTXprint binding key (if applicable)
            result["TODO_bindingType"] = s.trimBinding.bindingType
        return result

    def _mapLayout(self, s: WizardState) -> Dict[str, Any]:
        result = {}
        if s.layout.columns is not None:
            # TODO(integrate): map columns -> PTXprint columns setting key
            result["TODO_columns"] = s.layout.columns
        if s.layout.bodyFontSize is not None:
            # TODO(integrate): map bodyFontSize -> PTXprint body font size key
            result["TODO_bodyFontSize"] = s.layout.bodyFontSize
        if s.layout.bodyLeading is not None:
            # TODO(integrate): map bodyLeading -> PTXprint line spacing key
            result["TODO_bodyLeading"] = s.layout.bodyLeading
        if s.layout.bodyFont is not None:
            # TODO(integrate): map bodyFont -> PTXprint body font key
            result["TODO_bodyFont"] = s.layout.bodyFont
        if s.layout.marginPreset is not None:
            # TODO(integrate): map marginPreset -> PTXprint margin keys (top/bottom/inner/outer)
            result["TODO_marginPreset"] = s.layout.marginPreset
        return result

    def _mapContent(self, s: WizardState) -> Dict[str, Any]:
        result = {}
        if s.content.scope is not None:
            # TODO(integrate): map scope -> PTXprint book selection / scope key
            result["TODO_contentScope"] = s.content.scope
        if s.content.selectedBooks:
            # TODO(integrate): map selectedBooks -> PTXprint book list key
            result["TODO_selectedBooks"] = s.content.selectedBooks
        if s.content.isDiglot:
            # TODO(integrate): map isDiglot -> PTXprint diglot mode key
            result["TODO_isDiglot"] = True
            if s.content.secondaryProject:
                # TODO(integrate): map secondaryProject -> PTXprint secondary project key
                result["TODO_secondaryProject"] = s.content.secondaryProject
        if s.content.isTriglot:
            result["TODO_isTriglot"] = True
            if s.content.tertiaryProject:
                result["TODO_tertiaryProject"] = s.content.tertiaryProject
        return result

    def _mapPeripherals(self, s: WizardState) -> Dict[str, Any]:
        result = {}
        # TODO(integrate): map each peripheral ID -> PTXprint peripheral toggle key
        for periph in s.peripherals.selected:
            result[f"TODO_peripheral_{periph}"] = True
        return result

    def computeDiff(self, currentConfig: Dict[str, Any],
                    newSettings: Dict[str, Any]) -> List[Tuple[str, Any, Any]]:
        """Return [(key, oldValue, newValue), ...] for every setting that changes."""
        diff = []
        allKeys = set(currentConfig) | set(newSettings)
        for key in sorted(allKeys):
            oldVal = currentConfig.get(key)
            newVal = newSettings.get(key)
            if oldVal != newVal:
                diff.append((key, oldVal, newVal))
        return diff
