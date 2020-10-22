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

