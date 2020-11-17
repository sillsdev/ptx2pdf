import re
from ptxprint.minidialog import MiniCheckButton
from ptxprint.utils import _

class ScriptSnippet:
    dialogstruct = None

    @classmethod
    def regexes(cls, model):
        return []

    @classmethod
    def tex(cls, model):
        return ""

class mymr(ScriptSnippet):
    dialogstruct = [
        MiniCheckButton("c_scrmymrSyllable", _("Syllable line breaking"))
    ]

    @classmethod
    def regexes(cls, model):
        res = [(None, re.compile(r'(\s)/'), r'\1'),
               (None, re.compile(r'([\u00AB\u2018\u201B\u201C\u201F\u2039\u2E02\u2E04\u2E09\u2E0C\u2E1C\u2E20])/'), r'\1', re.S),
               (None, re.compile(r'/([\u00BB\u2019\u201D\u203A\u2E03\u2E05\u2E0A\u2E0D\u2E1D\u2E21])'), r'\1', re.S),
               (None, re.compile(r'/([\s\u104A\u104B])'), r'\1', re.S),
               (None, re.compile(r'/'), "\u200B")]
        if model["scrmymr/syllables"]:
            res += [(None, re.compile('(?<![\\s\u1039])([\u1000-\u1022\uAA61-\uAA6F\uAA71])(?!\uFE00?[\\s\u1039\u103A])'), '\u200B\\1')]
        return res

class thai(ScriptSnippet):
    @classmethod
    def regexes(cls, model):
        res = [(None, re.compile(r'(\s)/'), r'\1'),
               (None, re.compile(r'/([\s\u0E46])'), r'\1'),
               (None, re.compile(r'/'), "\u200B")]
        return res

