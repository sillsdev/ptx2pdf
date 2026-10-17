# Translation memory recovered from the git history of a language's .po file, plus fuzzy matching.
import difflib
import re
import subprocess

from poLib import parsePoText


def normalise(s):
    return re.sub(r'\s+', ' ', s).strip().lower()


class History:
    """msgid -> newest non-empty historic translation, built by walking `git log` newest first."""

    def __init__(self, repoRoot, relPath, maxCommits=60):
        self.tm = {}            # msgid -> (msgstr, commit)
        self.commits = 0
        r = subprocess.run(['git', 'log', '--format=%H', '-n', str(maxCommits), '--', relPath], cwd=repoRoot,
                           capture_output=True, text=True, encoding='utf-8')
        for h in r.stdout.split():
            g = subprocess.run(['git', 'show', '{}:{}'.format(h, relPath)], cwd=repoRoot,
                               capture_output=True, text=True, encoding='utf-8')
            if g.returncode != 0:
                continue
            self.commits += 1
            for e in parsePoText(g.stdout):
                if e.msgid and e.msgstr.strip() and e.msgid not in self.tm:
                    self.tm[e.msgid] = (e.msgstr, h[:9])
        self._norm = None

    def exact(self, msgid):
        if msgid in self.tm:
            return self.tm[msgid][0]
        n = normalise(msgid)
        for k, v in self.tm.items():            # same text apart from whitespace/case
            if normalise(k) == n:
                return v[0]
        return None

    def closest(self, msgid, minRatio=0.6):
        """Most similar historic English string with a translation: (oldMsgid, oldMsgstr, ratio) or None."""
        if self._norm is None:
            self._norm = [(normalise(k), k) for k in self.tm]
        n = normalise(msgid)
        sm = difflib.SequenceMatcher(autojunk=False)
        sm.set_seq2(n)
        best = None
        for kn, k in self._norm:
            if abs(len(kn) - len(n)) > 0.5 * max(len(kn), len(n)):
                continue
            sm.set_seq1(kn)
            if sm.real_quick_ratio() < minRatio or sm.quick_ratio() < minRatio:
                continue
            r = sm.ratio()
            if r >= minRatio and (best is None or r > best[2]):
                best = (k, self.tm[k][0], r)
        return best
