#!/usr/bin/env python3
# Builds locales/<lang>/lexicon.tsv: the established translation of PTXprint's recurring terms, learned by reading
# the language's existing .po. poTranslate.py feeds the matching rows to the model so new strings reuse the same words.
#
#   python buildLexicon.py --lang fr --command <claude.exe>
#   python buildLexicon.py --lang es --terms 300 --history      # also mine older git versions of the .po
import argparse
import json
import os
import re
import sys
from collections import Counter

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from poLib import parsePo                                       # noqa: E402
from providers import makeProvider                              # noqa: E402
from poTranslate import loadConfig, localesDir, repoRoot        # noqa: E402

stopWords = set("""a an and are as at be by for from if in into is it its of on or that the this to up use used using
with when will you your can not do does only then than also any all each other which where while after before
should would could may must have has had been being per via here there so but no yes""".split())

PROMPT = """Below are English terms from the user interface of PTXprint (Bible typesetting software) and example \
strings where the {lang} translators used them. Work out the established {lang} rendering of each term.

For each term reply with:
- "term": the English term exactly as given
- "translation": the {lang} word or phrase the translators normally use for it (dictionary form, as it would appear \
in a label). If they usually leave it in English, give the English word.
- "alt": other renderings that also occur (empty string if none)
- "note": at most 8 words, only if useful (e.g. "noun" or "verb: to fill"); otherwise empty

Base the answer only on how the examples render the term; do not substitute your own preferred word. If the term \
means different things in different examples, give the main sense and mention the other in "alt".
Reply with ONLY a JSON array.

<terms>
{terms}
</terms>"""


def candidates(entries, nTerms):
    docs = Counter()
    for e in entries:
        words = re.findall(r"[A-Za-z][A-Za-z'-]+", e.msgid)
        if len(words) > 8:
            continue
        low = [w.lower() for w in words]
        grams = set()
        for i, w in enumerate(low):
            if w not in stopWords and len(w) > 2:
                grams.add(w)
            if i + 1 < len(low) and low[i] not in stopWords and low[i + 1] not in stopWords:
                grams.add(low[i] + ' ' + low[i + 1])
        docs.update(grams)
    return [t for t, c in docs.most_common() if c >= 3][:nTerms], docs


def examples(term, entries, n=6):
    rx = re.compile(r'(?<![A-Za-z])' + re.escape(term) + r"(?![A-Za-z])", re.I)
    hits = [e for e in entries if rx.search(e.msgid)]
    hits.sort(key=lambda e: len(e.msgid))
    return [{'en': e.msgid.replace('\n', ' '), 'tr': e.msgstr.replace('\n', ' ')} for e in hits[:n]]


def parseReply(text):
    text = re.sub(r'^```(?:json)?|```$', '', text.strip(), flags=re.M)
    a, b = text.find('['), text.rfind(']')
    return json.loads(text[a:b + 1])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--lang', required=True)
    ap.add_argument('--config', default=os.path.join(here, 'localize.toml'))
    ap.add_argument('--provider')
    ap.add_argument('--command', help="path to the claude executable")
    ap.add_argument('--terms', type=int, default=250, help="how many recurring terms to analyse")
    ap.add_argument('--batch', type=int, default=25)
    ap.add_argument('--history', action='store_true', help="add older translations from git history as examples")
    args = ap.parse_args()

    cfg = loadConfig(args.config)
    if args.command:
        for p in cfg['providers'].values():
            if p.get('type') == 'claudeCli':
                p['command'] = args.command
    lc = cfg['languages'][args.lang]
    provName = args.provider or lc.get('provider') or cfg.get('defaults', {}).get('provider', 'claude')
    provider = makeProvider(provName, cfg['providers'][provName])

    langDir = os.path.join(localesDir, args.lang)
    entries = [e for e in parsePo(os.path.join(langDir, 'LC_MESSAGES', 'ptxprint.po')) if e.msgid and e.msgstr.strip()]
    if args.history:
        from historyLib import History
        have = {e.msgid for e in entries}
        hist = History(repoRoot, 'python/locales/{}/LC_MESSAGES/ptxprint.po'.format(args.lang))
        from poLib import Entry
        for k, (tr, _) in hist.tm.items():
            if k not in have:
                e = Entry()
                e.msgid, e.msgstr = k, tr
                entries.append(e)
    terms, docs = candidates(entries, args.terms)
    print("[{}] {} entries, analysing {} terms via '{}'".format(args.lang, len(entries), len(terms), provName))

    rows = {}
    for n in range(0, len(terms), args.batch):
        chunk = terms[n:n + args.batch]
        payload = json.dumps([{'term': t, 'examples': examples(t, entries)} for t in chunk],
                             ensure_ascii=False, indent=1)
        prompt = PROMPT.format(lang=lc.get('name', args.lang), terms=payload)
        for attempt in range(3):
            try:
                for r in parseReply(provider.complete(prompt)):
                    rows[r['term'].lower()] = r
                break
            except Exception as ex:
                print("    attempt {} failed: {}".format(attempt + 1, str(ex)[:150]))
        print("  {}/{}".format(min(n + args.batch, len(terms)), len(terms)))

    out = os.path.join(langDir, 'lexicon.tsv')
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write("# Auto-built by buildLexicon.py from the existing {} translations. Do not hand-edit:\n"
                "# put overrides in glossary.tsv (which wins). English<TAB>translation<TAB>note\n".format(args.lang))
        for t in terms:
            r = rows.get(t.lower())
            if not r or not r.get('translation'):
                continue
            note = '; '.join(x for x in [('also: ' + r['alt']) if r.get('alt') else '', r.get('note', '')] if x)
            f.write("{}\t{}\t{}\n".format(t, r['translation'].replace('\t', ' '), note.replace('\t', ' ')))
    print("[{}] wrote {} ({} terms)".format(args.lang, out, len(rows)))


if __name__ == '__main__':
    main()
