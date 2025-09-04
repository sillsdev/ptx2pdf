import regex, traceback
from ptxprint.minidialog import MiniCheckButton
from usfmtc.reference import Environment
from ptxprint.utils import _

def makeChange(pattern, to, flags=0, context=None):
    frame =  traceback.extract_stack(limit=2)[0]
    return (context, regex.compile(pattern, flags), to, f"{frame.filename} line {frame.lineno}")

class ScriptSnippet:
    dialogstruct = None
    refenv = Environment

    @classmethod
    def regexes(cls, view):
        return []

    @classmethod
    def tex(cls, view):
        return ""

    @classmethod
    def getrefenv(cls, view):
        return cls.refenv

    @classmethod
    def isSyllableBreaking(cls, view):
        return False

    @classmethod
    def indicSyls(cls):
        res = []
        # Define nonWordChars to also exclude the hyphenChar
        # (Variable name beginning with 'g' indicates Grouping parentheses used.)
        nonWordChar = r"(?:[^\u003d" + cls.hyphenChar + cls.wordChars + "])"
        gNonWordChar = r"([^\u003d" + cls.hyphenChar + cls.wordChars + "]|^|$)"

        # components of syllable patterns
        consPattern = "[" + cls.cons + "][" + cls.cmodifiers + "]*"
        viramasPattern = "[" + cls.viramas + r"][\u200c\u200d\u0324]*"  # Temporarily included: 0324 (combining diaeresis) until permanent nukta is available
        optMatras = "[" + cls.matras + cls.vmodifiers + "]*"

        # Syllable patterns
        syllPattern1 = "(?:(?:" + consPattern + viramasPattern + ")*" + consPattern + optMatras + ")"
        syllPattern2 = "(?:(?:" + consPattern + viramasPattern + ")*" + consPattern + viramasPattern + "(?=" + nonWordChar + "))"
        syllPattern3 = "(?:[" + cls.indVowels + "][" + cls.vmodifiers + "]*)"
        gSyllPattern = "(" + syllPattern1 + "|" + syllPattern2 + "|" + syllPattern3 + ")"

        res += [makeChange(gSyllPattern, cls.hyphenChar + r'\1', context=onlybody)]                  # Begin by inserting a break before EVERY syllable
        res += [makeChange(gNonWordChar + cls.hyphenChar, r'\1', context=onlybody)]                  # Remove break at start of word
        res += [makeChange(gNonWordChar + gSyllPattern + cls.hyphenChar, r'\1\2', context=onlybody)] # Remove break after 1st syllable (need 2 syll before break.)
        res += [makeChange(cls.hyphenChar + gSyllPattern + gNonWordChar, r'\1\2', context=onlybody)] # Remove break before last syllable (need 2 syll after break.)
        res += [makeChange(cls.hyphenChar + r"(?=[\u0d7a-\u0d7f])", '', context=onlybody)]           # Remove break before MAL atomic chillu  \u0d7a-\u0d7f
        res += [makeChange(cls.hyphenChar + r"(?=[\u0d23\u0d28\u0d30\u0d32\u0d33\u0d15]\u0d4d\u200d)", '', context=onlybody)] # Remove break before MAL old-style chillu 
        return res

#nonbodymarkers = ("id", "h", "h1", "toc1", "toc2", "toc3", "mt1", "mt2")
nonbodymarkers = ("id", "h", "h1")    # keep in toc to allow wrapping

def onlybody(fn, bj, dat):
    res = []
    for l in dat.split("\n"):
        m = regex.match(r"^\\(\S+) ", l)
        if m:
            if m.group(1) in nonbodymarkers:
                res.append(l)
                continue
        res.append(fn(l))
    return "\n".join(res)

def nonbody(fn, bj, dat):
    res = []
    for l in dat.split("\n"):
        m = regex.match(r"^\\(\S+) ", l)
        if m:
            if m.group(1) not in nonbodymarkers:
                res.append(l)
                continue
        res.append(fn(l))
    return "\n".join(res)

def notattrib(fn, bj, dat):
    #if "/" in dat:
    #    import pdb; pdb.set_trace()
    b = regex.split(r"((?<!\\)\|.*?\\[a-z*])", dat)
    for i, w in enumerate(b[0::2]):
        b[2*i] = fn(w)
    return "".join(b)

class Indic(ScriptSnippet):
    dialogstruct = [
        MiniCheckButton("c_scrindicSyllable", _("Syllable line breaking")),
        MiniCheckButton("c_scrindicshowhyphen", _("Show Hyphen"))
    ]

    @classmethod
    def isSyllableBreaking(self, view):
        return view.get("c_scrindicSyllable")

class mymr(ScriptSnippet):
    dialogstruct = [
        MiniCheckButton("c_scrmymrSyllable", _("Syllable line breaking"))
    ]

    @classmethod
    def isSyllableBreaking(self, view):
        return view.get("c_scrmymrSyllable")

    @classmethod
    def regexes(cls, view):
        res = [makeChange(r'(\s)/', r'\1'),
               makeChange('([\u00AB\u2018\u201B\u201C\u201F\u2039\u2E02\u2E04\u2E09\u2E0C\u2E1C\u2E20])/', r'\1', regex.S),
               makeChange('/([\u00BB\u2019\u201D\u203A\u2E03\u2E05\u2E0A\u2E0D\u2E1D\u2E21])', r'\1', regex.S),
               makeChange('/([\\s\u104A\u104B])', r'\1', regex.S),
               makeChange(r'/', "\u200B", context=notattrib),
               makeChange('\u200B', "", context=nonbody)]
        if view.get("c_scrmymrSyllable"):
            cons = "[\u1000-\u102A\u103F\u104C-\u1055\u105A-\u105D\u1061\u1065\u1066\u106E-\u1070\u1075-\u1081" + \
                   "\u108E\u109E\u109F\uA9E0-\uA9E4\uA9E7-\uA9EF\uA9F8-\uA9FE\uAA60-\uAA6F" + \
                   "\uAA71-\uAA7A\uAA7E\uAA7F]\uFE00?"
            ncons = "[\u102B-\u103E\u1056-\u1059\u105E-\u1060\u1062-\u1064\u1067-\u106D\u1071-\u1074" + \
                    "\u1082-\u108D\u108F\u109A-\u109D\uA9E5\uA9E6\uAA70\uAA7B-\uAA7D]|\u1039{}".format(cons)
            res += [makeChange('(?<![\\s\u1039"\'\\[\\(\\{{\u2018-\u201F])({0})(?!(?:{1})*[\\s\u103A])'.format(cons, ncons), '\u200B\\1', context=onlybody)]
            res += [makeChange('(\u103A\u1039{0})\u200B'.format(cons), r'\1', context=onlybody)]
            res += [makeChange('(\\s{0}(?:\u1039{0})*(?:{1})*)\u200B'.format(cons, ncons), r'\1', context=onlybody)]
        return res

class thai(ScriptSnippet):
    @classmethod
    def regexes(cls, view):
        res = [makeChange(r'(\s)/', r'\1'),
               makeChange('/([\\s\u0E46])', r'\1'),
               makeChange(r'/', "\u200B", context=notattrib),
               makeChange(r'([^\u0E00-\u0E7F])\u200B', r'\1'),
               makeChange(r'\u200B([^\\\u0E00-\u0E7F])', r'\1'),
               makeChange('\u200B', "", context=nonbody)]
        return res

class laoo(ScriptSnippet):
    @classmethod
    def regexes(cls, view):
        res = [makeChange(r'(\s)/', r'\1'),
               makeChange('/([\\s\u0EC6])', r'\1'),
               makeChange(r'/', "\u200B", context=notattrib),
               makeChange(r'([^\u0E80-\u0EFF])\u200B', r'\1'),
               makeChange(r'\u200B([^\\\u0E80-\u0EFF])', r'\1'),
               makeChange('\u200B', "", context=nonbody)]
        return res

class lana(ScriptSnippet):
    @classmethod
    def regexes(cls, view):
        res = [makeChange(r'(\s)/', r'\1'),
               makeChange('/([\\s\u1AA7])', r'\1'),
               makeChange(r'/', "\u200B", context=notattrib),
               makeChange(r'([^\u1A20-\u1A7F])\u200B', r'\1'),
               makeChange(r'\u200B([^\\\u1A20-\u1A7F])', r'\1'),
               makeChange('\u200B', "", context=nonbody)]
        return res

class talu(ScriptSnippet):
    @classmethod
    def regexes(cls, view):
        res = [makeChange(r'/', "\u200B", context=notattrib),
               makeChange(r'([^\u1980-\u19DF])\u200B', r'\1'),
               makeChange(r'\u200B([^\\\u1980-\u19DF])', r'\1'),
               makeChange('\u200B', "", context=nonbody)]
        return res

class arab(ScriptSnippet):
    dialogstruct = [
        MiniCheckButton("c_scrarabrefs", _("First verse on left"))
    ]
    refseparators = (Environment(rangemk="\u200F-", cvsep="\u200F:", versesep="\u060C ", chapsep="\u061B "),
                     Environment(rangemk="\u200F-", cvsep="\u200F:", versesep="\u060C ", chapsep="\u061B "))

    @classmethod
    def getrefseps(cls, view):
        return cls.refseparators[1 if view.get("c_scrarabrefs") else 0]

class mlym(Indic):
    @classmethod
    def regexes(cls, view):
        res = []
        if view.get("c_scrindicSyllable"):
            cls.hyphenChar = '\u00AD' if view.get("c_scrindicshowhyphen") else '\u200B'
            cls.indVowels = r'\u0d05-\u0d14\u0d60\u0d61'
            cls.vmodifiers = r'\u0d02-\u0d03\u0d3d\u0324'
            cls.cmodifiers = r'\u0324'
            cls.cons = r'\u0d15-\u0d39\u0d7a-\u0d7f'
            cls.matras = r'\u0d3e-\u0d4c\u0d57\u0d62\u0d63'
            cls.viramas = r'\u0d4d'
            cls.wordChars = r'\u0d01-\u0d63\u0d7a-\u0d7f\u200c\u200d\u0324'
            res = cls.indicSyls()
        return res

class taml(Indic):
    @classmethod
    def regexes(cls, view):
        res = []
        if view.get("c_scrindicSyllable"):
            cls.hyphenChar = '\u00AD' if view.get("c_scrindicshowhyphen") else '\u200B'
            cls.wordChars = r'\u0b81-\u0be3'
            cls.cons = r'\u0b95-\u0bb9'
            cls.indVowels = r'\u0b85-\u0b94'
            cls.matras = r'\u0bbc-\u0bcc\u0bd7\u0bcd'
            # cls.viramas = r'\u0bcd' # this behaves more like a vowel matra (keep with prev cons)
            cls.viramas = r''
            cls.cmodifiers = r'\u0324'
            cls.vmodifiers = r'\u0b82'
            res = cls.indicSyls()
            res += [makeChange(r"{}([\u0b95-\u0bb9]\u0bcd)".format(cls.hyphenChar), r"\1")]
        return res
            
class sinh(Indic):
    @classmethod
    def regexes(cls, view):
        res = []
        if view.get("c_scrindicSyllable"):
            cls.hyphenChar = '\u00AD' if view.get("c_scrindicshowhyphen") else '\u200B'
            cls.wordChars = r'\u0d81-\u0df3'
            cls.cons = r'\u0d9a-\u0dc6'
            cls.indVowels = r'\u0d85-\u0d96'
            cls.matras = r'\u0dcf-\u0df3'
            cls.viramas = r'\u0dca'
            cls.cmodifiers = r'\u0324'
            cls.vmodifiers = r'\u0d82'
            res = cls.indicSyls()
        return res
            
class telu(Indic):
    @classmethod
    def regexes(cls, view):
        res = []
        if view.get("c_scrindicSyllable"):
            cls.hyphenChar = '\u00AD' if view.get("c_scrindicshowhyphen") else '\u200B'
            cls.wordChars = r'\u0c01-\u0c63\u0c7f'
            cls.cons = r'\u0c15-\u0c39\u0c58\u0c59'
            cls.indVowels = r'\u0c05-\u0c14\u0c60\u0c61'
            cls.matras = r'\u0c3e-\u0c4c\u0c55\u0c56\u0c62\u0c63'
            cls.viramas = r'\u0c4d'
            cls.cmodifiers = r'\u0324'
            cls.vmodifiers = r'\u0c01-\u0c03\u0c4d'
            res = cls.indicSyls()
        return res
            
class knda(Indic):
    @classmethod
    def regexes(cls, view):
        res = []
        if view.get("c_scrindicSyllable"):
            cls.hyphenChar = '\u00AD' if view.get("c_scrindicshowhyphen") else '\u200B'
            cls.wordChars = r'\u0c81-\u0ce3\u0cf1\u0cf2'
            cls.cmodifiers = r'\u0324\u0cbc'  # KAN nukta
            cls.cons = r'\u0c95-\u0cb9\u0cde'
            cls.indVowels = r'\u0c85-\u0c94\u0ce0\u0ce1'
            cls.matras = r'\u0cbe-\u0ccc\u0cd5\u0cd6\u0ce2\u0ce3'
            cls.viramas = r'\u0ccd'
            cls.vmodifiers = r'\u0c82-\u0c83\u0cbd'
            res = cls.indicSyls()
        return res
            
class orya(Indic):
    @classmethod
    def regexes(cls, view):
        res = []
        if view.get("c_scrindicSyllable"):
            cls.hyphenChar = '\u00AD' if view.get("c_scrindicshowhyphen") else '\u200B'
            cls.wordChars = r'\u0b01-\u0b63\u0b70\u0b71'
            cls.cmodifiers = r'\u0324\u0b3c'  # ORI nukta
            cls.cons = r'\u0b15-\u0b39\u0b5c\u0b5d\u0b5f\u0b70\u0b71'
            cls.indVowels = r'\u0b05-\u0b14\u0b60\u0b61'
            cls.matras = r'\u0b3e-\u0b4c\u0b56\u0b57\u0b62\u0b63'
            cls.viramas = r'\u0b4d'
            cls.vmodifiers = r'\u0b01-\u0b03\u0b4d'  
            res = cls.indicSyls()
        return res

class beng(ScriptSnippet):
    @classmethod
    def regexes(cls, view):
        res = [
            #makeChange("(?<=\\s)([\u0985-\u09CC](?![\u09C7-\u09CC])[^\\\\\\s]*?"
            #           "[\u09C7-\u09CC][^\\\\\\s]*?)(?=\\s)", "\uFDEC\\1\uFDED")
            makeChange("(?<=[\u0980-\u09CC\u09CE-\u09FF])([\u0985-\u09B9]\u09BC?"
                        "(?:\u09CD[\u0985-\u09B9]\u09BC?)*)(?=[\u09C7-\u09CC])",
                        "\uFDD0\\1", context=onlybody)
            ]
        return res

class hans(ScriptSnippet):
    dialogstruct = [
        MiniCheckButton("c_scrcjkgrid", _("Enabling horizontal gridding"),
                tip=_("Align chapter numbers with grid and remove spaces before verses")),
        MiniCheckButton("c_scrcjkhalfpunc", _("Automatic halfwidth punctuation pairs"),
                tip=_("Adjust spacing of punctuation pairs so they take up a single full width character"))
    ]
    @classmethod
    def regexes(cls, view):
        res = []
        if view.get("c_scrcjkgrid", False):
            res.append(makeChange(r"(?<!\\\S+)\s+(?=\\v\s)", ""))
        if view.get("c_scrcjkhalfpunc", False):
            res.append(makeChange(r"([\p{Po}\p{Pe}\p{Pf}--[*\\]])(\\f\s(?:.(?!\\f\*))*.\\f\*)([\p{Po}\p{Pe}\p{Pf}--[*\\]])", r"\1\3\2", flags=regex.V1))
            res.append(makeChange(r"([\p{Pe}\p{Pf}\p{Po}--[*\\]])([\p{Ps}\p{Pi}])", r"\\cjksqm\1\2", flags=regex.V1))
            res.append(makeChange(r"([\p{Ps}\p{Pi}])([\p{Ps}\p{Po}\p{Pi}--[*\\]])", r"\\cjksq\1\2", flags=regex.V1))
            res.append(makeChange(r"([\p{Pe}\p{Pf}])([\p{Pe}\p{Pf}\p{Po}--[*\\]])", r"\\cjksq\1\2", flags=regex.V1))
            res.append(makeChange(r"([\p{Po}--[*\\]])([\p{Pe}\p{Pf}])", r"\\cjksq\1\2", flags=regex.V1))
        return res

    @classmethod
    def tex(cls, view):
        res = []
        if view.get("c_scrcjkgrid", False):
            res.append(r"\cjkgridchapterbox")
        if view.get("c_scrcjkhalfpunc", False):
            res.append(r"\def\cjksq#1#2{#1\kern-.5em #2\kern-.5em}")
            res.append(r"\def\cjksqm#1#2{#1\kern-1em #2}")
        return "\n".join(res)

class hant(hans):
    pass


