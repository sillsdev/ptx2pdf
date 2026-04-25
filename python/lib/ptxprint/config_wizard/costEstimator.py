import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

UNKNOWN = "unknown"


def _whenMatches(flat: Dict[str, Any], when: Dict[str, Any]) -> bool:
    for key, expected in when.items():
        actual = flat.get(key)
        if actual is None and expected != {}:
            return False
        if isinstance(expected, list):
            if actual not in expected:
                return False
        elif isinstance(expected, dict):
            if "min" in expected and (actual is None or actual < expected["min"]):
                return False
            if "max" in expected and (actual is None or actual > expected["max"]):
                return False
        elif expected != {} and actual != expected:
            return False
    return True


class CostEstimator:

    def __init__(self, dataDir: Path):
        self._perCopyRules: List[Dict] = []
        self._totalRules: List[Dict] = []
        self._loaded = False
        self._load(dataDir / "costRules.json")

    def _load(self, path: Path) -> None:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._perCopyRules = data.get("perCopy", [])
            self._totalRules = data.get("total", [])
            self._loaded = True
        except FileNotFoundError:
            logger.error(f"costRules.json not found at {path}")
        except Exception as e:
            logger.error(f"Failed to load costRules.json: {e}")

    def _firstMatch(self, rules: List[Dict], flat: Dict[str, Any]) -> str:
        for rule in rules:
            if _whenMatches(flat, rule.get("when", {})):
                return rule.get("value", UNKNOWN)
        return UNKNOWN

    def estimate(self, flat: Dict[str, Any]) -> Tuple[str, str]:
        """Return (perCopy, total) each as 'low'|'medium'|'high'|'unknown'."""
        if not self._loaded:
            return (UNKNOWN, UNKNOWN)
        return (
            self._firstMatch(self._perCopyRules, flat),
            self._firstMatch(self._totalRules, flat),
        )
