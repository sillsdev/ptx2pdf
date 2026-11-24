''' Compares a configuration's settings in one project (the reference) with the configuration of
    the same name in other projects, and copies chosen settings across.

    Settings that belong to a project or a publication (its variables, publications, which
    projects a diglot uses, which book was last chosen...) are not compared: they are meant to
    differ. Styles (ptxprint.sty) are not compared either.
'''

import os, configparser
from dataclasses import dataclass
from typing import Optional
from ptxprint.manager.validate import readConfig

NOTSET = None       # the config doesn't have the setting (so PTXprint uses its default)

# sections that are a project's own
ownSections = ("vars", "strongsvars", "vars.publishable", "import", "config", "coverwiz")
ownPrefixes = ("publication.", "diglot_")
ownSettings = {("project", "id"), ("project", "book"), ("project", "booklist"), ("project", "bookscope"),
               ("project", "modulefile"), ("project", "copyright"), ("project", "license"), ("project", "printcount"),
               ("document", "chapfrom"), ("document", "chapto"), ("document", "subject"), ("document", "toctitle"),
               ("document", "title"), ("document", "author"), ("document", "diffpdf"), ("document", "diglotsecprj"),
               ("document", "diglotsecprjguid"), ("document", "diglotsecconfig"),
               ("cover", "totalpages"), ("cover", "spinewidth"), ("paper", "watermarkpdf"),
               ("project", "frontincludes"), ("project", "backincludes"), ("project", "selectxrfile"),
               ("texpert", "bottomrag"), ("strongsndx", "fallbackprj"),
               ("poly", "fraction")}        # how wide this project's column of a diglot is

def isShared(sect, opt):
    ''' Is this a setting that would normally be the same in every project using the configuration? '''
    if sect in ownSections or any(sect.startswith(p) for p in ownPrefixes):
        return False
    if (sect, opt) in ownSettings or opt.startswith("_"):
        return False
    return True

@dataclass
class Difference:
    section: str
    option: str
    project: str
    value: Optional[str]            # what the project has, or NOTSET
    refValue: Optional[str]         # what the reference has, or NOTSET

    @property
    def setting(self):
        return f"{self.section}/{self.option}"

    @property
    def oneSided(self):
        return self.value is NOTSET or self.refValue is NOTSET


class Comparison:

    def __init__(self, validator, cfg, reference):
        self.validator = validator
        self.cfg = cfg
        self.reference = reference
        self.refSettings = self.settingsOf(reference)

    def cfgPath(self, prjid):
        return os.path.join(self.validator.configDir(prjid, self.cfg), "ptxprint.cfg")

    def settingsOf(self, prjid):
        config = readConfig(self.cfgPath(prjid))
        return {(s, o): v for s in config.sections() for o, v in config.items(s) if isShared(s, o)}

    def differences(self, prjids):
        ''' Returns the Differences of these projects from the reference, by setting then project '''
        res = []
        for prjid in prjids:
            if prjid == self.reference or self.cfg not in self.validator.configNames(prjid):
                continue
            try:
                mine = self.settingsOf(prjid)
            except (configparser.Error, OSError):
                continue
            for key in set(mine) | set(self.refSettings):
                a = mine.get(key, NOTSET)
                b = self.refSettings.get(key, NOTSET)
                if a != b and not self.sameValue(a, b):
                    res.append(Difference(key[0], key[1], prjid, a, b))
        res.sort(key=lambda d: (d.section, d.option, d.project.lower()))
        return res

    @staticmethod
    def sameValue(a, b):
        ''' 0.5 and 0.50, True and true: written differently by different versions, but the same '''
        if a is NOTSET or b is NOTSET:
            return False
        if a.strip().lower() == b.strip().lower():
            return True
        if "${" in a and a.replace("\\", "/") == b.replace("\\", "/"):       # the same file
            return True
        try:
            return abs(float(a) - float(b)) < 1e-6
        except ValueError:
            return False

    def copy(self, differences):
        ''' Give each difference's project the reference's value. Returns how many settings were changed. '''
        byProject = {}
        for d in differences:
            byProject.setdefault(d.project, []).append(d)
        done = 0
        for prjid, ds in byProject.items():
            path = self.cfgPath(prjid)
            config = readConfig(path)
            for d in ds:
                ref = self.refSettings.get((d.section, d.option), NOTSET)
                if ref is NOTSET:
                    if config.has_option(d.section, d.option):
                        config.remove_option(d.section, d.option)
                else:
                    if not config.has_section(d.section):
                        config.add_section(d.section)
                    config.set(d.section, d.option, ref)
                done += 1
            with open(path, "w", encoding="utf-8") as outf:
                config.write(outf)
        return done
