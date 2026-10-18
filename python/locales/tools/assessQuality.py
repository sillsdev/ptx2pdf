#!/usr/bin/env python3
# Samples a language's existing translations and has the model grade them, plus cheap mechanical checks.
# Writes locales/<lang>/work/quality.tsv and prints a summary.
#
#   python assessQuality.py --lang ar ro tpi zh --sample 120 --command <claude.exe>
import argparse
import json
import os
import random
import re
import sys
from collections import Counter

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from poLib import parsePo, isTranslatable, checkTranslation    # noqa: E402
from providers import makeProvider                              # noqa: E402
from poTranslate import loadConfig, localesDir                  # noqa: E402

PROMPT = """You are a bilingual reviewer (English and {lang}) assessing existing translations of the user interface of \
PTXprint, desktop software that typesets Bible translations. Users are Bible translators and typesetters who \
know common English computing words, so loanwords such as font, PDF, file are fine.

Grade each item's {lang} translation:
- "good": accurate, clear and natural.
- "ok": understandable and correct in meaning, but stiff, clumsy or slightly unnatural.
- "poor": hard to understand, partly wrong, or reads like word-by-word machine translation.
- "wrong": means something different from the English, is nonsense, or is left untranslated by mistake.

Be strict about meaning: check the actual sense in a Bible-typesetting context, not just whether the words exist. \
Reply with ONLY a JSON array: [{{"id": 1, "grade": "good"}}, {{"id": 2, "grade": "wrong", "reason": "<=12 words", \
"better": "an improved translation"}}]. Give "reason" and "better" only for poor/wrong.

<items>
{items}
</items>"""


def kindOf(msgid):
    if '\n' in msgid or len(msgid) > 70:
        return 'tooltip'
    if '{}' in msgid or '%' in msgid:
        return 'message'
    return 'label'


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--lang', nargs='+', required=True)
    ap.add_argument('--sample', type=int, default=120)
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--batch', type=int, default=20)
    ap.add_argument('--config', default=os.path.join(here, 'localize.toml'))
    ap.add_argument('--provider')
    ap.add_argument('--command')
    ap.add_argument('--po', default='ptxprint.po', help="file in LC_MESSAGES to assess (e.g. ptxprint.new.po)")
    args = ap.parse_args()
    cfg = loadConfig(args.config)
    if args.command:
        for p in cfg['providers'].values():
            if p.get('type') == 'claudeCli':
                p['command'] = args.command
    for lang in args.lang:
        lc = cfg['languages'][lang]
        provName = args.provider or lc.get('provider') or cfg.get('defaults', {}).get('provider', 'claude')
        provider = makeProvider(provName, cfg['providers'][provName])
        entries = [e for e in parsePo(os.path.join(localesDir, lang, 'LC_MESSAGES', args.po)) if e.msgid]
        tr = [e for e in entries if isTranslatable(e.msgid)]
        done = [e for e in tr if e.msgstr.strip()]
        scriptRe = re.compile(lc['script']) if lc.get('script') else None

        # mechanical checks over everything
        same = [e for e in done if e.msgstr.strip() == e.msgid.strip() and sum(c.isalpha() for c in e.msgid) > 4
                and not re.fullmatch(r'[A-Za-z0-9 ,.:;()/_+\-\[\]]*', e.msgid.strip()) is None and len(e.msgid) > 12]
        noScript = [e for e in done if scriptRe and sum(c.isalpha() for c in e.msgid) > 12 and not scriptRe.search(e.msgstr)]
        bad = [e for e in done if checkTranslation(e.msgid, e.msgstr)]
        print("\n=== {} ({}) ===".format(lang, lc['name']))
        print("translatable {}, empty {} ({:.0f}%), placeholder/markup problems {}, identical to English {}, "
              "no {} script {}".format(len(tr), len(tr) - len(done), 100 * (len(tr) - len(done)) / len(tr), len(bad),
                                      len(same), lc['name'], len(noScript)))

        # model grading of a stratified random sample
        rnd = random.Random(args.seed)
        groups = {'label': [], 'tooltip': [], 'message': []}
        for e in done:
            groups[kindOf(e.msgid)].append(e)
        per = {'label': args.sample * 2 // 5, 'tooltip': args.sample * 2 // 5, 'message': args.sample // 5}
        sample = []
        for k, g in groups.items():
            sample += rnd.sample(g, min(per[k], len(g)))
        rnd.shuffle(sample)
        grades = Counter()
        byKind = {k: Counter() for k in groups}
        rows = []
        for n in range(0, len(sample), args.batch):
            chunk = sample[n:n + args.batch]
            items = [{'id': i, 'en': e.msgid, lang: e.msgstr} for i, e in enumerate(chunk)]
            prompt = PROMPT.format(lang=lc['name'], items=json.dumps(items, ensure_ascii=False, indent=1))
            for attempt in range(3):
                try:
                    txt = provider.complete(prompt)
                    arr = json.loads(re.search(r'\[.*\]', txt, re.S).group(0))
                    break
                except Exception as ex:
                    print("   retry:", str(ex)[:100])
                    arr = []
            for o in arr:
                e = chunk[int(o['id'])]
                g = o.get('grade', '?')
                grades[g] += 1
                byKind[kindOf(e.msgid)][g] += 1
                rows.append((g, kindOf(e.msgid), e.msgid, e.msgstr, o.get('reason', ''), o.get('better', '')))
        total = sum(grades.values())
        print("graded {}: ".format(total) + ', '.join("{} {} ({:.0f}%)".format(g, grades[g], 100 * grades[g] / total)
                                                     for g in ('good', 'ok', 'poor', 'wrong') if total))
        for k, c in byKind.items():
            t = sum(c.values())
            if t:
                print("   {:8} n={:3}  good+ok {:.0f}%  poor+wrong {:.0f}%".format(
                    k, t, 100 * (c['good'] + c['ok']) / t, 100 * (c['poor'] + c['wrong']) / t))
        out = os.path.join(localesDir, lang, 'work', 'quality-' + args.po.replace('.po', '') + '.tsv')
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, 'w', encoding='utf-8', newline='\n') as f:
            f.write("grade\tkind\tenglish\tcurrent\treason\tbetter\n")
            for r in sorted(rows, key=lambda r: ['wrong', 'poor', 'ok', 'good'].index(r[0]) if r[0] in
                            ('wrong', 'poor', 'ok', 'good') else 9):
                f.write('\t'.join(x.replace('\n', '\\n').replace('\t', ' ') for x in r) + '\n')
        print("report:", out)


if __name__ == '__main__':
    main()
