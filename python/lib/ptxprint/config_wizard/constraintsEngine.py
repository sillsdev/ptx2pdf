import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .wizardState import WizardState, SectionStatus

logger = logging.getLogger(__name__)


def _matchValue(actual: Any, expected: Any) -> bool:
    """Return True if actual satisfies the expected constraint."""
    if actual is None:
        return False
    if isinstance(expected, list):
        return actual in expected
    if isinstance(expected, dict):
        ok = True
        if "min" in expected and actual < expected["min"]:
            ok = False
        if "max" in expected and actual > expected["max"]:
            ok = False
        return ok
    return actual == expected


def _whenMatches(flat: Dict[str, Any], when: Dict[str, Any]) -> bool:
    """Return True if all when-clause conditions match."""
    for key, expected in when.items():
        actual = flat.get(key)
        if not _matchValue(actual, expected):
            return False
    return True


class ConstraintsEngine:

    def __init__(self, dataDir: Path):
        self._rules: List[Dict] = []
        self._filterRules: List[Dict] = []
        self._dependencies: List[Dict] = []
        self._fieldDefs: Dict[str, Dict] = {}
        self._sectionRequiredFields: Dict[str, List[str]] = {}
        self._loaded = False
        self._load(dataDir / "constraints.json")

    def _load(self, path: Path) -> None:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._rules = data.get("rules", [])
            self._filterRules = data.get("filterRules", [])
            self._dependencies = data.get("dependencies", [])
            self._fieldDefs = data.get("fields", {})
            self._sectionRequiredFields = data.get("sectionRequiredFields", {})
            self._loaded = True
        except FileNotFoundError:
            logger.error(f"constraints.json not found at {path}")
        except Exception as e:
            logger.error(f"Failed to load constraints.json: {e}")

    def isLoaded(self) -> bool:
        return self._loaded

    def allowedValues(self, fieldKey: str, flat: Dict[str, Any]) -> Optional[List[Any]]:
        """Return allowed values for fieldKey given current flat state, or None if unrestricted."""
        fieldDef = self._fieldDefs.get(fieldKey, {})
        baseValues = fieldDef.get("values")

        for rule in self._filterRules:
            if rule.get("field") != fieldKey:
                continue
            if _whenMatches(flat, rule.get("when", {})):
                allowed = rule.get("allowedValues", [])
                if baseValues:
                    allowed = [v for v in baseValues if v in allowed]
                return allowed

        return baseValues

    def evaluateRules(self, flat: Dict[str, Any], estimatedPageCount: int = 0) -> List[Dict]:
        """Return list of violated rules: [{id, severity, message}, ...]"""
        extFlat = dict(flat)
        extFlat["estimatedPageCount"] = estimatedPageCount

        violations = []
        for rule in self._rules:
            when = rule.get("when", {})
            require = rule.get("require", {})
            if not _whenMatches(extFlat, when):
                continue
            # when matches — check require
            for reqKey, reqVal in require.items():
                actual = extFlat.get(reqKey)
                if not _matchValue(actual, reqVal):
                    violations.append({
                        "id": rule["id"],
                        "severity": rule.get("severity", "warning"),
                        "message": rule.get("message", ""),
                    })
                    break
        return violations

    def sectionStatus(self, sectionId: str, flat: Dict[str, Any],
                      violations: List[Dict], previousStatus: str,
                      dependencyChanged: bool) -> SectionStatus:
        """Compute the status badge for a section."""
        required = self._sectionRequiredFields.get(sectionId, [])
        allFilled = all(flat.get(f) is not None for f in required)

        sectionViolations = [v for v in violations
                             if any(f.startswith(sectionId) for f in required)
                             or sectionId in v.get("id", "").lower()]

        hasErrors = any(v["severity"] == "error" for v in sectionViolations)
        hasWarnings = any(v["severity"] == "warning" for v in sectionViolations)

        if previousStatus == SectionStatus.complete and dependencyChanged:
            return SectionStatus.stale

        if not required:
            if hasErrors:
                return SectionStatus.hasWarnings
            return SectionStatus.complete

        if not allFilled:
            anyFilled = any(flat.get(f) is not None for f in required)
            return SectionStatus.inProgress if anyFilled else SectionStatus.notStarted

        if hasErrors:
            return SectionStatus.inProgress

        if hasWarnings:
            return SectionStatus.hasWarnings

        return SectionStatus.complete

    def dependsOn(self, sectionId: str) -> List[str]:
        for dep in self._dependencies:
            if dep.get("section") == sectionId:
                return dep.get("dependsOn", [])
        return []
