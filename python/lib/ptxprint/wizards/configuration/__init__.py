"""PTXprint Publication Wizard.

Standalone usage
----------------
    python -m ptxprint.wizards.configuration <projectDir> <configName> [--version <ver>]

Called from PTXprint
--------------------
    from ptxprint.wizards.configuration import launchWizard
    launchWizard(ptxprintModel, parentWindow=win,
                 projectDir=model.project.path, configName=model.cfgid,
                 ptxprintVersion=VersionStr, onApply=model.updateUI)
"""


def launchWizard(model, parentWindow=None, projectDir="", configName="Default",
                 ptxprintVersion="", onApply=None):
    """Launch the wizard and return the Gtk.ResponseType when it closes.

    Parameters
    ----------
    model : ViewModel / GtkViewModel or None
        The live PTXprint model. Pass None to run without writing to a model.
    parentWindow : Gtk.Window or None
    projectDir : str
        Root of the Paratext project directory.
    configName : str
        PTXprint configuration name.
    ptxprintVersion : str
    onApply : callable or None
        Called with the final answers dict after settings are written.
    """
    from ptxprint.wizards.configuration.wizardController import WizardController
    ctrl = WizardController(
        model=model,
        projectDir=projectDir,
        configName=configName,
        parentWindow=parentWindow,
        ptxprintVersion=ptxprintVersion,
        onApply=onApply,
    )
    return ctrl.run()


def _main():
    import argparse
    import sys
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk

    try:
        from ptxprint.utils import setup_i18n
        setup_i18n()
    except ImportError:
        pass

    ap = argparse.ArgumentParser(description="PTXprint Publication Wizard (standalone)")
    ap.add_argument("projectDir", nargs="?", default=".",
                    help="Paratext project directory (default: current directory)")
    ap.add_argument("configName", nargs="?", default="Default",
                    help="PTXprint configuration name (default: Default)")
    ap.add_argument("--version", default="", dest="ptxprintVersion",
                    help="PTXprint version string written to wizardState.json")
    ap.add_argument("--dry-run", action="store_true",
                    help="Open the wizard but do not write settings to a model")
    args = ap.parse_args()

    model = None
    if not args.dry_run:
        # Try to load a real ViewModel for the project so settings are actually applied
        try:
            from ptxprint.view import ViewModel
            model = ViewModel()
            model.setup_ini()
        except Exception as e:
            print("Warning: could not load PTXprint model ({!s}). Running in dry-run mode.".format(e))
            model = None

    resp = launchWizard(
        model=model,
        parentWindow=None,
        projectDir=args.projectDir,
        configName=args.configName,
        ptxprintVersion=args.ptxprintVersion,
    )
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk
    sys.exit(0 if resp == Gtk.ResponseType.OK else 1)


if __name__ == "__main__":
    _main()
