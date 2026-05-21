from dataclasses import dataclass, field
from typing import List, Optional, Tuple


@dataclass
class Warning:
    severity: str          # "soft"
    questionIds: List[str]
    message: str


VOLUME_BANDS = {
    "homeInkjet":    "low",
    "officeLaser":   "low",
    "photocopyShop": "mediumLow",
    "podLow":        "mediumLow",
    "podHigh":       "mediumHigh",
    "offset":        "high",
}


def volumeBandForPrinter(printer: str) -> Optional[str]:
    return VOLUME_BANDS.get(printer)


def validate(answers: dict) -> List[Warning]:
    """Return a list of cross-question warnings. Never blocks; never hides options."""
    warnings = []
    pageCount = answers.get("pageCount")
    binding   = answers.get("binding")
    printer   = answers.get("printer")
    om        = answers.get("outputMedium", "print")
    colour    = answers.get("colour")
    pt        = answers.get("productType")

    if pageCount is not None and binding:
        if pageCount > 1500 and binding == "saddleStitch":
            warnings.append(Warning("soft", ["pageCount", "binding"],
                "Saddle-stitch binding does not work for books this thick."))
        if pageCount < 32 and binding == "perfect":
            warnings.append(Warning("soft", ["pageCount", "binding"],
                "Perfect binding needs at least 32 pages. Your page count looks too low."))
        if pageCount < 64 and binding == "hardcover":
            warnings.append(Warning("soft", ["pageCount", "binding"],
                "Hardcover binding needs at least 64 pages. Your page count looks too low."))

    if om == "digital" and colour == "blackAndWhite":
        warnings.append(Warning("soft", ["outputMedium", "colour"],
            "Most screens can show colour. Are you sure you want black-and-white?"))

    if pt == "lifeApplicationBible":
        warnings.append(Warning("soft", ["productType"],
            "This layout uses extra study material. Make sure your project includes it before publishing."))

    return warnings


def evaluateCondition(condition, answers: dict) -> bool:
    """Evaluate a condition dict. Supports simple answers-clause and compound anyOf/allOf/not."""
    if condition is None:
        return True
    if "anyOf" in condition:
        return any(evaluateCondition(c, answers) for c in condition["anyOf"])
    if "allOf" in condition:
        return all(evaluateCondition(c, answers) for c in condition["allOf"])
    if "not" in condition:
        return not evaluateCondition(condition["not"], answers)
    answersClause = condition.get("answers", {})
    for qid, expected in answersClause.items():
        actual = answers.get(qid)
        if not _matchValue(actual, expected):
            return False
    return True


def evaluateShowIf(condition, answers: dict) -> bool:
    return evaluateCondition(condition, answers)


def evaluateDisableIf(disableIf, answers: dict) -> bool:
    """Return True if the option should be *disabled* (legacy v1 disableIf support)."""
    if not disableIf:
        return False
    for clause in disableIf.get("anyOf", []):
        if evaluateCondition(clause, answers):
            return True
    return False


_STRICTNESS = {"notAdvised": 3, "notOptimal": 2, "recommended": 1}


def evaluateRecommendIf(option: dict, answers: dict) -> Tuple[Optional[str], Optional[str]]:
    """Evaluate recommendIf rules for an option.

    Returns (level, reason) where level is 'recommended', 'notOptimal', 'notAdvised', or None.
    When multiple rules fire, the strictest level wins.
    """
    rules = option.get("recommendIf", [])
    result_level = None
    result_reason = None
    for rule in rules:
        level = rule.get("level")
        when  = rule.get("when")
        reason = rule.get("reason", "")
        if evaluateCondition(when, answers):
            if result_level is None or _STRICTNESS.get(level, 0) > _STRICTNESS.get(result_level, 0):
                result_level = level
                result_reason = reason
    return result_level, result_reason


def _matchValue(actual, expected):
    if isinstance(expected, dict):
        if "in" in expected:
            return actual in expected["in"]
        if "gt" in expected and not (actual is not None and actual > expected["gt"]):
            return False
        if "lt" in expected and not (actual is not None and actual < expected["lt"]):
            return False
        if "gte" in expected and not (actual is not None and actual >= expected["gte"]):
            return False
        if "lte" in expected and not (actual is not None and actual <= expected["lte"]):
            return False
        if "between" in expected:
            a, b = expected["between"]
            if not (actual is not None and a <= actual <= b):
                return False
        if "contains" in expected:
            if not (actual is not None and expected["contains"] in actual):
                return False
        return True
    if isinstance(actual, list):
        return expected in actual
    return actual == expected


def resolveDefault(question: dict, answers: dict):
    """Return the resolved default value for a question given current answers."""
    default = question.get("default")
    if not isinstance(default, dict) or "rules" not in default:
        return default
    for rule in default["rules"]:
        if evaluateCondition(rule.get("if", {}), answers):
            return rule["then"]
    return default.get("else")


def visibleOptions(question: dict, answers: dict) -> list:
    """Return options visible for the question (showOnlyIf filtering + rankBy + recommendIf badges)."""
    options = [
        opt for opt in question.get("options", [])
        if evaluateCondition(opt.get("showOnlyIf"), answers)
    ]
    rankBy = question.get("rankBy", [])
    if rankBy:
        promoted = []
        for rule in rankBy:
            # Each rankBy entry is a condition dict (has "answers" key) + "promote" list
            if evaluateCondition(rule, answers):
                promoted.extend(rule.get("promote", []))
        if promoted:
            top  = [o for o in options if o["id"] in promoted]
            rest = [o for o in options if o["id"] not in promoted]
            options = top + rest
    return options
