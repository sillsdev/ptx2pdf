#!/usr/bin/env python3
# Lists existing translations whose placeholders / markup / paragraph breaks don't match the English.
# Writes locales/<lang>/work/audit.tsv for each language (english, current, problems) and prints a summary.
#
#   python auditPo.py                 # all languages
#   python auditPo.py --lang th tpi
import argparse
import glob
import os
import sys
from collections import Counter

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from poLib import parsePo, isTranslatable, checkTranslation    # noqa: E402

localesDir = os.path.dirname(here)


def flat(t):
    return t.replace('\n', '\\n').replace('\t', ' ')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--lang', nargs='*')
    args = ap.parse_args()
    for f in sorted(glob.glob(os.path.join(localesDir, '*', 'LC_MESSAGES', 'ptxprint.po'))):
        lang = os.path.basename(os.path.dirname(os.path.dirname(f)))
        if lang == 'en' or (args.lang and lang not in args.lang):
            continue
        kinds = Counter()
        rows = []
        for e in parsePo(f):
            if not e.msgid or not e.msgstr or not isTranslatable(e.msgid):
                continue
            errs = checkTranslation(e.msgid, e.msgstr)
            if errs:
                for x in errs:
                    kinds[x.split(':')[0]] += 1
                rows.append((e.msgid, e.msgstr, '; '.join(errs)))
        out = os.path.join(localesDir, lang, 'work', 'audit.tsv')
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, 'w', encoding='utf-8', newline='\n') as w:
            w.write("english\tcurrent\tproblems\n")
            for r in rows:
                w.write('\t'.join(flat(x) for x in r) + '\n')
        print("{:4} {:4} problems  {}".format(lang, len(rows), dict(kinds)))


if __name__ == '__main__':
    main()
