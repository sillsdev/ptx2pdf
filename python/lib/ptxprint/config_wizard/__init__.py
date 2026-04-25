"""
PTXprint Setup Wizard package.

Usage from PTXprint:

    from ptxprint.config_wizard import SetupWizardApp

    # Launch as modal dialog (parent = main PTXprint Gtk.Window):
    app = SetupWizardApp(parent=main_window, projectDir=Path(project_path))
    app.run()

    # Auto-launch on empty project:
    SetupWizardApp.launch(parent=main_window, projectDir=Path(project_path), autoLaunch=True)
"""

from pathlib import Path
from typing import Optional

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .wizardWindow import WizardWindow

import logging
logger = logging.getLogger(__name__)

_DATA_DIR = Path(__file__).parent / "data"


class SetupWizardApp:
    """
    Entry point for the PTXprint Setup Wizard.
    Mirrors the interface of CoverWizardApp for consistency.
    """

    def __init__(self, parent: Optional[Gtk.Window] = None,
                 projectDir: Optional[Path] = None,
                 autoLaunch: bool = False):
        statePath = None
        if projectDir:
            statePath = Path(projectDir) / "wizardState.json"

        self._window = WizardWindow(
            parent=parent,
            dataDir=_DATA_DIR,
            statePath=statePath,
            autoLaunch=autoLaunch,
        )

    def run(self):
        """Show the wizard. Non-blocking; integrates with the existing GTK main loop."""
        self._window.run()

    @classmethod
    def launch(cls, parent: Optional[Gtk.Window] = None,
               projectDir: Optional[Path] = None,
               autoLaunch: bool = False) -> "SetupWizardApp":
        """Convenience factory — create and immediately run the wizard."""
        app = cls(parent=parent, projectDir=projectDir, autoLaunch=autoLaunch)
        app.run()
        return app
