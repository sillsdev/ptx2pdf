import json
import os
import datetime
import logging

logger = logging.getLogger(__name__)

STATE_VERSION = 2


def statePath(projectDir, configName):
    """Return the path to wizardState.json for the given project/config."""
    return os.path.join(projectDir, "shared", "ptxprint", configName, "wizardState.json")


def loadState(projectDir, configName):
    """Load wizard state. Returns {} if the file does not exist or is unreadable."""
    path = statePath(projectDir, configName)
    if not os.path.exists(path):
        return {}
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return {}
        return _migrate(data)
    except Exception as e:
        logger.warning("Could not load wizard state from %s: %s", path, e)
        return {}


def saveState(projectDir, configName, answers, ptxprintVersion=""):
    """Persist wizard answers to disk. Returns True on success."""
    path = statePath(projectDir, configName)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = {
        "version": STATE_VERSION,
        "savedAt": datetime.datetime.utcnow().isoformat() + "Z",
        "ptxprintVersion": ptxprintVersion,
        "configName": configName,
        "answers": answers,
    }
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error("Could not save wizard state to %s: %s", path, e)
        return False


def deleteState(projectDir, configName):
    """Delete wizardState.json. Returns True if deleted, False if it was not there."""
    path = statePath(projectDir, configName)
    if os.path.exists(path):
        try:
            os.remove(path)
            return True
        except Exception as e:
            logger.error("Could not delete wizard state at %s: %s", path, e)
    return False


def _migrate(data):
    version = data.get("version", 1)
    answers = data.get("answers", {})
    if version < 2:
        answers.pop("volume", None)   # volume question removed in v2
    return answers
