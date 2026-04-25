"""
Standalone test runner for the PTXprint Setup Wizard.

Run from the repo root with:

    python -m ptxprint.config_wizard

Or call the helper function directly in a Python session:

    from ptxprint.config_wizard.__main__ import runWizardStandalone
    runWizardStandalone()
"""

import sys
import logging
from pathlib import Path

logging.basicConfig(level=logging.DEBUG,
                    format="%(levelname)s  %(name)s  %(message)s")
logger = logging.getLogger(__name__)


def runWizardStandalone(projectDir: str = None, dataDir: str = None):
    """
    Launch the Setup Wizard as a standalone GTK application for testing.

    Args:
        projectDir:  Path to a (real or dummy) project directory.
                     Used to read/write wizardState.json.
                     Pass None to use a temporary location.
        dataDir:     Override the data directory (constraints, recipes, etc.).
                     Defaults to config-wizard/data/ next to this file.

    Example:
        python -m ptxprint.config_wizard
        python -m ptxprint.config_wizard --project /path/to/project
    """
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk

    from pathlib import Path as _Path

    thisDir = _Path(__file__).parent
    resolvedData = _Path(dataDir) if dataDir else thisDir / "data"
    resolvedState = (_Path(projectDir) / "wizardState.json") if projectDir else None

    logger.info(f"Starting standalone wizard")
    logger.info(f"  data dir : {resolvedData}")
    logger.info(f"  state    : {resolvedState or '(no save path)'}")

    from .wizardWindow import WizardWindow

    win = WizardWindow(
        parent=None,
        dataDir=resolvedData,
        statePath=resolvedState,
        autoLaunch=False,
    )

    # Connect destroy to quit the main loop
    win._win.connect("destroy", Gtk.main_quit)
    win._win.show_all()
    Gtk.main()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="PTXprint Setup Wizard — standalone test")
    parser.add_argument("--project", metavar="DIR",
                        help="Project directory (for wizardState.json save/resume)")
    parser.add_argument("--data", metavar="DIR",
                        help="Override data directory (constraints, recipes, etc.)")
    args = parser.parse_args()

    runWizardStandalone(projectDir=args.project, dataDir=args.data)
