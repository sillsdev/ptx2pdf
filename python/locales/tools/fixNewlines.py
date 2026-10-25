#!/usr/bin/env python3
# msgfmt refuses a .po in which a translation begins or ends with a line break that the English does not
# (or the other way round), so no .mo can be built from it. This makes each translation begin and end with
# the same line breaks as its English, and leaves everything else alone.
#
#   python fixNewlines.py --lang all               # fixes <lang>/LC_MESSAGES/ptxprint.po in place
#   python fixNewlines.py --lang ko --file ptxprint.new.po
import argparse
import glob
import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from poLib import parsePo, writePo      # noqa: E402

localesDir = os.path.dirname(here)


def matchNewlines(msgid, msgstr):
    if not msgstr:
        return msgstr
    lead = len(msgid) - len(msgid.lstrip('\n'))
    trail = len(msgid) - len(msgid.rstrip('\n'))
    core = msgstr.strip('\n')
    if not core:
        return msgstr
    return '\n' * lead + core + '\n' * trail


def fixFile(path):
    entries = parsePo(path)
    fixed = 0
    for e in entries:
        if not e.msgid or not e.msgstr:
            continue
        new = matchNewlines(e.msgid, e.msgstr)
        if new != e.msgstr:
            e.msgstr = new
            fixed += 1
    if fixed:
        writePo(path, entries)
    return fixed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lang', nargs='+', required=True, help="language codes, or 'all'")
    ap.add_argument('--file', default='ptxprint.po', help="file in LC_MESSAGES")
    args = ap.parse_args()
    langs = args.lang
    if langs == ['all']:
        langs = sorted(os.path.basename(os.path.dirname(os.path.dirname(p)))
                       for p in glob.glob(os.path.join(localesDir, '*', 'LC_MESSAGES', args.file)))
    for lang in langs:
        path = os.path.join(localesDir, lang, 'LC_MESSAGES', args.file)
        if os.path.exists(path):
            print("{}: fixed {} line breaks".format(lang, fixFile(path)))


if __name__ == '__main__':
    main()
