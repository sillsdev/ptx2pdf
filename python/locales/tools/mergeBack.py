#!/usr/bin/env python3
# Restores earlier LLM translations into the current .po after a Crowdin sync replaced them.
# Three-way rule per msgid, using three versions of the language's .po:
#   base    the Crowdin text that Claude started from (a git commit before the Claude work)
#   mine    the Claude-localized version (a git commit)
#   current the file on disk now (Crowdin's latest download merged with the newest .pot)
#     current empty                 -> take mine (if it has one)
#     current == base               -> nobody edited it in Crowdin since: take mine (the Claude version)
#     current != base, non-empty    -> someone edited it in Crowdin since: keep current
# The result is written into <lang>/work/progress.json so that `poTranslate.py --lang X` only has to translate the
# strings that are still missing (new or reworded English), then writes the final .po.
#
#   python mergeBack.py --lang hi fr es            # (needs the git history that contains the Claude commits)
import argparse
import json
import os
import subprocess
import sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from poLib import parsePo, parsePoText, isTranslatable, checkTranslation          # noqa: E402
from poTranslate import loadConfig, localesDir, repoRoot                          # noqa: E402

BASE = 'febe51f47'                      # Crowdin sync of 2026-10-17, the text Claude started from
MINE = {'ar': 'd4633f973', 'ro': 'd4633f973', 'tpi': 'd4633f973', 'zh': 'd4633f973'}
MINE_DEFAULT = '61c96f079'


def gitPo(rev, lang):
    r = subprocess.run(['git', 'show', '{}:python/locales/{}/LC_MESSAGES/ptxprint.po'.format(rev, lang)],
                       cwd=repoRoot, capture_output=True, text=True, encoding='utf-8')
    if r.returncode != 0:
        raise SystemExit("cannot read {} at {}: {}".format(lang, rev, r.stderr.strip()))
    return {e.msgid: e.msgstr for e in parsePoText(r.stdout) if e.msgid}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--lang', nargs='+', required=True)
    ap.add_argument('--config', default=os.path.join(here, 'localize.toml'))
    ap.add_argument('--fromPo', action='store_true', help="use the current .po's string list instead of the .pot")
    args = ap.parse_args()
    cfg = loadConfig(args.config)
    for lang in args.lang:
        potFile = os.path.join(localesDir, lang, 'LC_MESSAGES', 'ptxprint.po') if args.fromPo else os.path.join(localesDir, 'ptxprint.pot')
        pot = [e.msgid for e in parsePo(potFile) if e.msgid]
        repl = cfg['languages'][lang].get('replace', [])
        base = gitPo(BASE, lang)
        mine = gitPo(MINE.get(lang, MINE_DEFAULT), lang)
        cur = {e.msgid: e.msgstr for e in parsePo(os.path.join(localesDir, lang, 'LC_MESSAGES', 'ptxprint.po')) if e.msgid}
        progress = {}
        stat = {'mine': 0, 'current': 0, 'missing': 0}
        for m in pot:
            if not isTranslatable(m):
                continue
            c, b, k = cur.get(m, ''), base.get(m), mine.get(m, '')
            if not c.strip():
                val, src = (k, 'mine') if k.strip() else ('', None)
            elif b is not None and c == b and k.strip():
                val, src = k, 'mine'
            else:
                val, src = c, 'current'
            for a, z in repl:
                val = val.replace(a, z)
            if src and not checkTranslation(m, val):
                progress[m] = {'msgstr': val, 'status': 'ok',
                               'provider': 'claude-restored' if src == 'mine' else 'crowdin-current'}
                stat[src] += 1
            else:
                stat['missing'] += 1
        p = os.path.join(localesDir, lang, 'work', 'progress.json')
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(progress, f, ensure_ascii=False, indent=0)
        print("{:4} restored from Claude {:5}  kept newer Crowdin {:4}  still to translate {:4}".format(
            lang, stat['mine'], stat['current'], stat['missing']))


if __name__ == '__main__':
    main()
