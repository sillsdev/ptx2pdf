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
               (None, re.compile('([\u00AB\u2018\u201B\u201C\u201F\u2039\u2E02\u2E04\u2E09\u2E0C\u2E1C\u2E20])/'), r'\1', re.S),
               (None, re.compile('/([\u00BB\u2019\u201D\u203A\u2E03\u2E05\u2E0A\u2E0D\u2E1D\u2E21])'), r'\1', re.S),
               (None, re.compile('/([\\s\u104A\u104B])'), r'\1', re.S),
               (None, re.compile(r'/'), "\u200B")]
        if model["scripts/mymr/syllables"]:
            cons = "[\u1000-\u102A\u103F\u104C-\u1055\u105A-\u105D\u1061\u1065\u1066\u106E-\u1070\u1075-\u1081" + \
                   "\u108E\u109E\u109F\uA9E0-\uA9E4\uA9E7-\uA9EF\uA9F8-\uA9FE\uAA60-\uAA6F" + \
                   "\uAA71-\uAA7A\uAA7E\uAA7F]\uFE00?"
            ncons = "[\u102B-\u103E\u1056-\u1059\u105E-\u1060\u1062-\u1064\u1067-\u106D\u1071-\u1074" + \
                    "\u1082-\u108D\u108F\u109A-\u109D\uA9E5\uA9E6\uAA70\uAA7B-\uAA7D]"
            res += [(None, re.compile('(?<![\\s\u1039"\'\[\(\{{\u2018-\u201F])({0})(?![\\s\u1039\u103A])'.format(cons)), '\u200B\\1')]
            res += [(None, re.compile('(\u103A\u1039{0})\u200B'.format(cons)), r'\1')]
            res += [(None, re.compile('(\\s{0}(?:\u1039{0})*{1}*)\u200B'.format(cons, ncons)), r'\1')]
        return res

class thai(ScriptSnippet):
    @classmethod
    def regexes(cls, model):
        res = [(None, re.compile(r'(\s)/'), r'\1'),
               (None, re.compile('/([\\s\u0E46])'), r'\1'),
               (None, re.compile(r'/'), "\u200B")]
        return res

