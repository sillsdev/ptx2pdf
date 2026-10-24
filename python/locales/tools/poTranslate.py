#!/usr/bin/env python3
# Context-aware LLM translation of locales/ptxprint.pot into locales/<lang>/LC_MESSAGES/*.po
#
#   python poTranslate.py --lang hi --limit 40 --onlyDone --out hi_trial.po
#   python poTranslate.py --lang hi                       # full run, resumable
#   python poTranslate.py --lang hi --provider lmstudio --batchSize 15
#   python poTranslate.py --lang hi --dryRun              # print the first prompt, call nothing
import argparse
import datetime
import json
import os
import re
import sys
import time

try:
    import tomllib
except ImportError:             # Python < 3.11
    import tomli as tomllib

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from poLib import parsePo, writePo, Entry, isTranslatable, fixWhitespace, checkTranslation   # noqa: E402
from contextLib import GladeIndex, CodeContext                                               # noqa: E402
from providers import makeProvider, ProviderError                                            # noqa: E402
from historyLib import History                                                               # noqa: E402

localesDir = os.path.dirname(here)
pythonDir = os.path.dirname(localesDir)
repoRoot = os.path.dirname(pythonDir)

PROMPT = """You are translating the user interface of PTXprint into {lang}. PTXprint is desktop software \
that typesets Bible translations (from Paratext projects) into print-ready PDFs. Its users are Bible \
translators and typesetters who already know common English computing words (font, margin, PDF).

Translate each English string in <items> into {lang}.

Rules:
- Keep every placeholder exactly as written: {{}}, {{0}}, %s, %d, %(name)s, doubled braces {{{{ }}}}, \
HTML-like tags, and backslash markers such as \\k or \\w. You may move a placeholder to where {lang} grammar \
needs it, but never drop, add or change one.
- Keep every blank line (paragraph break) of the English. Other line breaks may be reflowed; use \\n in JSON.
- Keep leading/trailing punctuation style (a trailing colon stays a colon, "..." stays an ellipsis).
- Menu/button/label strings must be short and natural. Tooltips may be full sentences.
- Use each item's "kind", "widget", "inside", "sameWidget" (other texts on the same control, such as its tooltip), "note" and "code" fields to decide the meaning of ambiguous words; \
do not translate those fields.
- Follow the style guide and glossary below. The glossary overrides your own choices.
- If an item has "previousEnglish" and "previousTranslation", the English was edited after that translation \
was made. Keep the wording and terminology of the previous translation and change only what the English edit \
requires.
- Do not add explanations or extra text.

{style}
{glossary}
{notes}
{extra}
Reply with ONLY a JSON array, one object per item, in this form: [{{"id": 12, "msgstr": "..."}}, ...]

<items>
{items}
</items>"""


def loadConfig(path):
    with open(path, 'rb') as f:
        return tomllib.load(f)


def readOptional(path):
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            return f.read().strip()
    return ''


class Glossary:
    """Reads glossary.tsv (hand-written, wins) then lexicon.tsv (built by buildLexicon.py) from a language folder."""

    def __init__(self, *paths):
        self.rows = []
        seen = set()
        for path in paths:
            if not os.path.exists(path):
                continue
            with open(path, encoding='utf-8') as f:
                for line in f:
                    if not line.strip() or line.startswith('#'):
                        continue
                    cols = line.rstrip('\n').split('\t')
                    if len(cols) >= 2 and cols[0].lower() not in seen:
                        seen.add(cols[0].lower())
                        self.rows.append((cols[0], cols[1], cols[2] if len(cols) > 2 else ''))

    def forBatch(self, texts):
        low = ' \n '.join(t.lower() for t in texts)
        return [r for r in self.rows if re.search(r'(?<![a-z])' + re.escape(r[0].lower()) + r'(?![a-z])', low)]

    def render(self, rows, notes=False):
        if not rows:
            return ''
        if notes:
            out = ["Meaning of PTXprint terms (translate the MEANING into the target language, not these English words):"]
            out.extend("- {}: {}".format(en, tr) for en, tr, _ in rows)
            return '\n'.join(out) + '\n'
        out = ["Glossary (English -> required translation):"]
        for en, tr, note in rows:
            out.append("- {} -> {}{}".format(en, tr, " ({})".format(note) if note else ""))
        return '\n'.join(out) + '\n'


class Job:
    def __init__(self, args, cfg, lang):
        self.args = args
        self.lang = lang
        d = cfg.get('defaults', {})
        lc = cfg.get('languages', {}).get(lang, {})
        self.langName = lc.get('name', lang)
        self.scriptRe = re.compile(lc['script']) if lc.get('script') else None
        provName = args.provider or lc.get('provider') or d.get('provider', 'claude')
        self.provider = makeProvider(provName, cfg['providers'][provName])
        self.batchSize = args.batchSize or lc.get('batchSize') or d.get('batchSize', 40)
        self.maxRetries = lc.get('maxRetries', d.get('maxRetries', 2))
        self.useExisting = args.hints or lc.get('useExisting', d.get('useExisting', False))
        self.langDir = os.path.join(localesDir, lang)
        self.poDir = os.path.join(self.langDir, 'LC_MESSAGES')
        self.style = readOptional(os.path.join(self.langDir, 'style.md'))
        self.glossary = Glossary(os.path.join(self.langDir, 'glossary.tsv'), os.path.join(self.langDir, 'lexicon.tsv'))
        self.notes = Glossary(os.path.join(here, 'termNotes.tsv'))
        self.reuse = lc.get('reuseExisting', d.get('reuseExisting', False))
        self.replacements = lc.get('replace', [])      # [[from, to], ...] applied to every model answer
        self.previous = {}      # msgid -> (oldEnglish, oldTranslation, ratio) for strings whose English was edited
        self.progressPath = os.path.join(self.langDir, 'work', 'progress.json')
        self.progress = {}
        if os.path.exists(self.progressPath) and not args.redo:
            with open(self.progressPath, encoding='utf-8') as f:
                self.progress = json.load(f)

    # -- data ---------------------------------------------------------------
    def loadEntries(self, glade):
        # --fromPo: take the string list from the language's current .po (Crowdin's newer string set) instead of
        # the repo's ptxprint.pot, which can lag behind
        pot = parsePo(os.path.join(self.poDir, 'ptxprint.po') if self.args.fromPo
                      else os.path.join(localesDir, 'ptxprint.pot'))
        self.potHeader = pot[0] if pot and pot[0].msgid == '' else None
        self.potEntries = [e for e in pot if e.msgid != '']
        poPath = os.path.join(self.poDir, 'ptxprint.po')
        self.existing = {}
        self.poHeader = None
        if os.path.exists(poPath):
            old = parsePo(poPath)
            if old and old[0].msgid == '':
                self.poHeader = old[0]
            self.existing = {e.msgid: e.msgstr for e in old if e.msgid and e.msgstr}
        # glade order first so related widgets are batched together, then python messages by file
        big = 10 ** 9
        self.potEntries.sort(key=lambda e: (glade.order.get(e.msgid, big), e.refs[0] if e.refs else ''))

    def preload(self):
        """For languages with hand-polished translations: keep what exists, recover old translations from git
        history for strings that are now empty, and remember near matches so the model can adapt them."""
        kept = recovered = 0
        bad = []
        hist = History(repoRoot, 'python/locales/{}/LC_MESSAGES/ptxprint.po'.format(self.lang))
        print("[{}] history: {} commits, {} historic translations".format(self.lang, hist.commits, len(hist.tm)))
        for e in self.potEntries:
            if e.msgid in self.progress or not isTranslatable(e.msgid):
                continue
            cur = self.existing.get(e.msgid)
            if cur:
                for a, b in self.replacements:
                    cur = cur.replace(a, b)
                self.progress[e.msgid] = {'msgstr': cur, 'status': 'ok', 'provider': 'kept'}
                kept += 1
                if checkTranslation(e.msgid, cur):
                    bad.append(e.msgid)
                continue
            old = hist.exact(e.msgid)
            for a, b in self.replacements:
                old = old.replace(a, b) if old else old
            if old and not checkTranslation(e.msgid, old):
                self.progress[e.msgid] = {'msgstr': old, 'status': 'ok', 'provider': 'history'}
                recovered += 1
                continue
            near = hist.closest(e.msgid)
            if near:
                self.previous[e.msgid] = near
        print("[{}] kept {} existing, recovered {} from history, {} have an older version to adapt, "
              "{} existing translations fail the placeholder check".format(
                  self.lang, kept, recovered, len(self.previous), len(bad)))
        for m in bad[:10]:
            print("    check:", repr(m[:70]))

    def itemFor(self, idx, e, glade, code):
        it = {'id': idx, 'en': e.msgid}
        g = glade.lookup(e.msgid)
        if g:
            it['kind'] = g['kind']
            it['widget'] = (g['widget'] + ' ' if g['widget'] else '') + '({})'.format(g['cls'])
            same = glade.sameWidget(e.msgid)
            if same:
                it['sameWidget'] = same[:2]
            if g['path']:
                it['inside'] = ' > '.join(p for p in g['path'] if p)
            if g['note']:
                it['note'] = g['note']
        else:
            it['kind'] = 'program message'
            for r in e.refs:
                s = code.snippet(r)
                if s:
                    it['code'] = s
                    break
        for c in e.comments:
            if c.startswith('#.'):
                it['note'] = (it.get('note', '') + ' ' + c[2:].strip()).strip()
        if e.msgid in self.previous:
            it['previousEnglish'], it['previousTranslation'] = self.previous[e.msgid][:2]
        if self.useExisting and e.msgid in self.existing:
            it['currentTranslation'] = self.existing[e.msgid]
        return it

    # -- translation --------------------------------------------------------
    def buildPrompt(self, items, extra=''):
        texts = [i['en'] for i in items]
        return PROMPT.format(lang=self.langName,
                             style=("Style guide:\n" + self.style + "\n") if self.style else '',
                             glossary=self.glossary.render(self.glossary.forBatch(texts)),
                             notes=self.notes.render(self.notes.forBatch(texts), notes=True),
                             extra=extra,
                             items=json.dumps(items, ensure_ascii=False, indent=1))

    @staticmethod
    def parseReply(text):
        text = re.sub(r'^```(?:json)?|```$', '', text.strip(), flags=re.M)
        a, b = text.find('['), text.rfind(']')
        if a < 0 or b < a:
            raise ValueError("no JSON array in reply")
        arr = json.loads(text[a:b + 1])
        return {int(o['id']): o['msgstr'] for o in arr if 'id' in o and 'msgstr' in o}

    def askBatch(self, items, feedback=None):
        extra = ''
        if feedback:
            extra = ("Your previous answers for some items were rejected. Fix them:\n" +
                     '\n'.join("- id {}: {}".format(i, '; '.join(errs)) for i, errs in feedback.items()) + '\n')
        return self.parseReply(self.provider.complete(self.buildPrompt(items, extra)))

    def translateBatch(self, batch, glade, code):
        """batch: list of (idx, Entry). Returns {msgid: (msgstr, status)} where status is ok/fuzzy."""
        items = [self.itemFor(i, e, glade, code) for i, e in batch]
        byId = {i: e for i, e in batch}
        results = {}
        pending = {i: [] for i in byId}
        feedback = None
        best = {}
        for attempt in range(self.maxRetries + 1):
            sub = [it for it in items if it['id'] in pending]
            if not sub:
                break
            try:
                reply = self.askBatch(sub, feedback)
            except (ValueError, KeyError, json.JSONDecodeError, ProviderError) as ex:
                if isinstance(ex, ProviderError) and 'Cannot find' in str(ex):
                    raise
                print("    attempt {} failed: {}".format(attempt + 1, str(ex)[:200]))
                if attempt == self.maxRetries and len(batch) > 1:
                    mid = len(batch) // 2          # split a stubborn batch and try each half
                    results.update(self.translateBatch(batch[:mid], glade, code))
                    results.update(self.translateBatch(batch[mid:], glade, code))
                    return results
                continue
            feedback = {}
            for i in list(pending):
                if i not in reply:
                    feedback[i] = ["missing from reply"]
                    continue
                e = byId[i]
                tr = reply[i]
                for a, b in self.replacements:
                    tr = tr.replace(a, b)
                tr = fixWhitespace(e.msgid, tr)
                errs = checkTranslation(e.msgid, tr)
                best[i] = tr
                if errs:
                    feedback[i] = errs
                else:
                    results[e.msgid] = (tr, 'ok')
                    del pending[i]
        for i in pending:
            e = byId[i]
            if i in best:
                results[e.msgid] = (best[i], 'fuzzy')
        return results

    # -- output -------------------------------------------------------------
    def writeOutput(self, outPath, onlyDone):
        entries = []
        hdr = self.poHeader or self.potHeader or Entry()
        h = Entry()
        h.msgstr = hdr.msgstr
        h.msgstr = re.sub(r'(?m)^PO-Revision-Date:.*$',
                          'PO-Revision-Date: ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M%z'), h.msgstr)
        if 'X-Generator:' not in h.msgstr:
            h.msgstr += 'X-Generator: poTranslate.py ({})\n'.format(self.provider.name)
        entries.append(h)
        for e in self.potEntries:
            r = self.progress.get(e.msgid)
            o = Entry()
            o.refs, o.msgid = e.refs, e.msgid
            o.comments = [c for c in e.comments if c.startswith('#.')]
            if r:
                o.msgstr = r['msgstr']
                if r['status'] != 'ok':
                    o.flags.append('fuzzy')
            elif not isTranslatable(e.msgid) and e.msgid in self.existing:
                o.msgstr = self.existing[e.msgid]     # numbers, TeX code etc.: carry over untouched
            elif onlyDone:
                continue
            entries.append(o)
        writePo(outPath, entries)

    def saveProgress(self):
        os.makedirs(os.path.dirname(self.progressPath), exist_ok=True)
        with open(self.progressPath, 'w', encoding='utf-8') as f:
            json.dump(self.progress, f, ensure_ascii=False, indent=0)


def runLang(args, cfg, lang):
    job = Job(args, cfg, lang)
    glade = GladeIndex(os.path.join(pythonDir, 'lib', 'ptxprint', 'ptxprint.glade'))
    code = CodeContext(pythonDir)
    job.loadEntries(glade)
    if job.reuse:
        job.preload()
    outPath = args.out or os.path.join(job.poDir, 'ptxprint.new.po')
    if not os.path.isabs(outPath) and os.sep not in outPath and '/' not in outPath:
        outPath = os.path.join(job.poDir, outPath)

    todo = [(i, e) for i, e in enumerate(job.potEntries)
            if isTranslatable(e.msgid) and (args.match is None or re.search(args.match, e.msgid))
            and (e.msgid not in job.progress or job.progress[e.msgid]['status'] != 'ok')]
    todo = todo[args.offset:]
    if args.limit:
        todo = todo[:args.limit]
    print("[{}] {} strings to translate with provider '{}' (batch {}); output -> {}".format(
        lang, len(todo), job.provider.name, job.batchSize, outPath))
    if args.dryRun:
        if todo:
            batch = todo[:job.batchSize]
            print(job.buildPrompt([job.itemFor(i, e, glade, code) for i, e in batch]))
        return
    t0 = time.time()
    for n in range(0, len(todo), job.batchSize):
        batch = todo[n:n + job.batchSize]
        res = job.translateBatch(batch, glade, code)
        for msgid, (tr, status) in res.items():
            if job.scriptRe and status == 'ok' and sum(c.isalpha() for c in msgid) > 5 and not job.scriptRe.search(tr):
                print("    warning: no {} script in: {!r}".format(job.langName, tr[:60]))
            job.progress[msgid] = {'msgstr': tr, 'status': status, 'provider': job.provider.name}
        job.saveProgress()
        job.writeOutput(outPath, args.onlyDone)
        bad = sum(1 for v in res.values() if v[1] != 'ok')
        print("  {}/{} done ({} flagged fuzzy) {:.0f}s".format(min(n + job.batchSize, len(todo)), len(todo), bad,
                                                              time.time() - t0))
    job.writeOutput(outPath, args.onlyDone)
    print("[{}] wrote {}".format(lang, outPath))


REVIEW_PROMPT = """You are a careful reviewer of {lang} translations of the PTXprint user interface. PTXprint is desktop software that typesets Bible translations. Some were polished by hand and some came from a crowd-translation platform, so do not change mere style or synonym choices, but do fix real problems.

For each item decide:
- "keep": the translation is accurate and communicates clearly (do not change style or synonyms).
- "change": if it is wrong, misleading, hard to understand, reads like word-by-word machine translation, was left in English by mistake, damages a placeholder, or breaks the glossary or the style guide below (register, spelling, punctuation rules). Use the term meanings to judge the sense. Give the improved "msgstr" (changing as little as needed) and a short "reason".

{style}
{glossary}
{notes}
Reply with ONLY a JSON array: [{{"id": 12, "verdict": "keep"}}, {{"id": 13, "verdict": "change", "msgstr": "...", "reason": "..."}}]

<items>
{items}
</items>"""


def runReview(args, cfg, lang):
    """Ask the model whether existing translations are good. Writes work/review.tsv; changes are applied to the
    progress file (and so to the output .po) only with --applyReview. Resumable: reviewed strings are remembered
    in work/reviewed.json (use --redo to start again)."""
    job = Job(args, cfg, lang)
    glade = GladeIndex(os.path.join(pythonDir, 'lib', 'ptxprint', 'ptxprint.glade'))
    code = CodeContext(pythonDir)
    job.loadEntries(glade)
    job.useExisting = True
    if job.reuse:
        job.preload()
    reviewedPath = os.path.join(job.langDir, 'work', 'reviewed.json')
    reviewed = set()
    if os.path.exists(reviewedPath) and not args.redo:
        with open(reviewedPath, encoding='utf-8') as f:
            reviewed = set(json.load(f))
    todo = [(i, e) for i, e in enumerate(job.potEntries) if e.msgid in job.existing and isTranslatable(e.msgid)
            and e.msgid not in reviewed and (args.match is None or re.search(args.match, e.msgid))][args.offset:]
    if args.limit:
        todo = todo[:args.limit]
    print("[{}] reviewing {} existing translations ({} already reviewed) with '{}'".format(
        lang, len(todo), len(reviewed), job.provider.name))
    reportPath = os.path.join(job.langDir, 'work', 'review.tsv')
    os.makedirs(os.path.dirname(reportPath), exist_ok=True)
    fresh = not os.path.exists(reportPath) or args.redo or not reviewed
    outPath = args.out or os.path.join(job.poDir, 'ptxprint.new.po')
    changes = failed = 0
    with open(reportPath, 'w' if fresh else 'a', encoding='utf-8', newline='\n') as rep:
        if fresh:
            rep.write("english\tcurrent\tsuggested\treason\n")
        for n in range(0, len(todo), job.batchSize):
            batch = todo[n:n + job.batchSize]
            byId = {i: e for i, e in batch}
            items = [job.itemFor(i, e, glade, code) for i, e in batch]
            texts = [e.msgid for _, e in batch]
            prompt = REVIEW_PROMPT.format(lang=job.langName, items=json.dumps(items, ensure_ascii=False, indent=1),
                                          style=("Style guide:\n" + job.style + "\n") if job.style else '',
                                          glossary=job.glossary.render(job.glossary.forBatch(texts)),
                                          notes=job.notes.render(job.notes.forBatch(texts), notes=True))
            arr = None
            for attempt in range(3):
                try:
                    arr = json.loads(re.search(r'\[.*\]', job.provider.complete(prompt), re.S).group(0))
                    break
                except Exception as ex:
                    print("    batch attempt {} failed: {}".format(attempt + 1, str(ex)[:200]))
                    time.sleep(20 * (attempt + 1))
            if arr is None:
                failed += 1
                continue
            for o in arr:
                e = byId.get(int(o.get('id', -1)))
                if e is None or o.get('verdict') != 'change' or not o.get('msgstr'):
                    continue
                new = o['msgstr']
                for a, b in job.replacements:
                    new = new.replace(a, b)
                new = fixWhitespace(e.msgid, new)
                if checkTranslation(e.msgid, new) or new == job.existing[e.msgid]:
                    continue
                changes += 1
                flat = lambda t: t.replace('\n', '" "').replace('\t', ' ')
                rep.write('\t'.join([flat(e.msgid), flat(job.existing[e.msgid]), flat(new), o.get('reason', '')]) + '\n')
                if args.applyReview:
                    job.progress[e.msgid] = {'msgstr': new, 'status': 'ok', 'provider': 'review'}
            reviewed.update(texts)
            rep.flush()
            with open(reviewedPath, 'w', encoding='utf-8') as f:
                json.dump(sorted(reviewed), f, ensure_ascii=False)
            if args.applyReview:
                job.saveProgress()
                job.writeOutput(outPath, False)
            print("  {}/{} reviewed, {} suggested changes, {} batches failed".format(
                min(n + job.batchSize, len(todo)), len(todo), changes, failed))
    if args.applyReview:
        print("[{}] applied {} changes -> {}".format(lang, changes, outPath))
    print("[{}] report: {}{}".format(lang, reportPath, "  (" + str(failed) + " batches failed: rerun to retry)" if failed else ""))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--lang', action='append', required=True, help="language code (repeatable) or 'all'")
    ap.add_argument('--config', default=os.path.join(here, 'localize.toml'))
    ap.add_argument('--provider', help="override provider from the config")
    ap.add_argument('--command', help="path to the claude executable (overrides the config)")
    ap.add_argument('--batchSize', type=int)
    ap.add_argument('--limit', type=int, help="only translate this many strings (trial runs)")
    ap.add_argument('--offset', type=int, default=0)
    ap.add_argument('--match', help="only msgids matching this regex")
    ap.add_argument('--out', help="output file (bare name goes in the language's LC_MESSAGES)")
    ap.add_argument('--onlyDone', action='store_true', help="write only translated entries (for samples)")
    ap.add_argument('--hints', action='store_true', help="show current .po translations to the model as hints")
    ap.add_argument('--fromPo', action='store_true', help="use the string list of the current .po, not the .pot")
    ap.add_argument('--redo', action='store_true', help="ignore saved progress")
    ap.add_argument('--review', action='store_true', help="review existing translations (report only)")
    ap.add_argument('--applyReview', action='store_true', help="with --review: apply suggested changes to the output")
    ap.add_argument('--dryRun', action='store_true', help="print the first prompt and exit")
    args = ap.parse_args()
    cfg = loadConfig(args.config)
    if args.command:
        for p in cfg['providers'].values():
            if p.get('type') == 'claudeCli':
                p['command'] = args.command
    langs = args.lang
    if langs == ['all']:
        langs = sorted(cfg.get('languages', {}))
    for lang in langs:
        (runReview if args.review else runLang)(args, cfg, lang)


if __name__ == '__main__':
    main()
