# Based heavily on pypatgen, but restructured to allow more automation

from collections import defaultdict
from array import array
import multiprocessing
import random, re, sys

EMPTYSET = set()

DIGITS = "0123456789"
MISSED_HYPHEN = '.'
FALSE_HYPHEN = '*'
TRUE_HYPHEN = '-'
NOT_A_HYPHEN = ' '

default_weight = 1

def copypatterns(p):
    res = defaultdict(set)
    for k, v in p.items():
        res[k] = v.copy()
    return res

def stagger_range(start, end):
    middle = (start + end) // 2
    left = middle - 1
    right = middle + 1
    yield middle

    while left >= start or right < end:
        if left >= start:
            yield left
            left -= 1
        if right < end:
            yield right
            right += 1

def assess(m, f, inhibit, w, rng):
    return ((w * f + m) if inhibit else (w * m + f)) * rng * rng

def multi_predict(word, patterns, rng, mult, scores, maxrange, margins):
    word = "." + word + "."
    predictions = [defaultdict(set) for i in range(mult)]
    for chunklen in range(1, rng+1):
        for start in range(len(word) - chunklen + 1):
            ch = word[start:start+chunklen]
            allowed = patterns.get(ch, None)
            if allowed is None:
                continue
            left = margins[0] - start
            right = len(word) - margins[1] - start
            for index in range(rng+1):
                if not any(allowed[index::maxrange]) or index <= left or index >= right:
                    continue
                for m, s in enumerate(allowed[index::maxrange]):
                    for j in (v for v in scores[m] if v <= s):     # v is threshold
                        predictions[m][j].add(index + start - 1)
    return predictions

def predict(word, patterns, rng, maxrange, margins):
    word = "." + word + "."
    predictions = set()
    for chunklen in range(1, rng+1):
        for start in range(len(word) - chunklen + 1):
            ch = word[start:start+chunklen]
            allowed = patterns.get(ch, EMPTYSET)
            for index in allowed:
                if margins[0] < index + start < len(word) - margins[1]:
                    predictions.add(start + index - 1)
    return predictions

def score_predictions(item, getpool=multiprocessing.current_process):
    word, hyphens = item
    proc = getpool()
    nmissed = [{} for i in range(proc.mult)]
    nfalse = [{} for i in range(proc.mult)]
    predictions = multi_predict(word, proc.patterns, proc.rng, proc.mult, proc.scores, proc.maxrange, proc.margins)
    for mult, pred in enumerate(predictions):
        for score, p in pred.items():
            if not proc.inhibiting:
                misseds = proc.missed[word] - p
                falses = proc.false[word] | (p - hyphens)
            else:
                falses = proc.false[word] - p
                misseds = proc.missed[word] | (hyphens & (p - proc.missed[word]))
            nmissed[mult][score] = len(misseds)  # sum(self.d_weights[word][j] for j in misseds)
            nfalse[mult][score] = len(falses)    # sum(self.d_weights[word][j] for j in falses)
    return nmissed, nfalse

class Patgen:
    def __init__(self, maxrange=8, multiproc=None):
        self.patterns = []
        self.rngs = []
        self.selectors = []
        self.maxrange = maxrange
        self.settings = dict(HardHyphen="\u2010", SoftHyphen="-", SoftHyphenOut="-")
        self.hyphens = {}
        if multiproc is None:
            self.multiproc = sys.platform == "linux"
        else:
            self.multiproc = multiproc
        

    def load_dict(self, wlistfile, samples=2000):
        self.hyphens = {}     # ordereddict
        self.d_weights = {}
        self.d_missed = {}
        self.d_false = {}

        with open(wlistfile, encoding="utf-8") as inf:
            for l in inf.readlines():
                line = l.lstrip("\uFEFF").strip()
                if not line or line.startswith("#"):
                    continue
                m = re.match(r'^(\S+)\s=\s"([^"]+)"', line)
                if m:
                    self.settings[m[1]] = m[2]
                    continue
                text, hyphens, missed, false, weights = self._parse_dict_line(line.lower())
                self.hyphens[text] = hyphens
                self.d_weights[text] = weights
                self.d_missed[text] = missed | hyphens
                self.d_false[text] = false
        allhyphens = [(k, v) for k, v in self.hyphens.items() if len(v) > 0]
        self.d_hyphens = dict(random.choices(allhyphens, k=samples)) \
                    if 0 < samples < len(allhyphens) else self.hyphens
        self.missed = copypatterns(self.d_missed)
        self.false = copypatterns(self.d_false)

    def _parse_dict_line(self, word, texinput=False):
        text = []
        weights = {}
        hyphens = set()
        missed = set()
        false = set()

        word = word.lstrip("*")
        def_weight = 1
        if word[0] in DIGITS:
            def_weight = int(word[0])
        weights[0] = def_weight
        for c in word:
            if c == self.settings['SoftHyphen']:
                hyphens.add(len(text))
            elif texinput and c == MISSED_HYPHEN:
                hyphens.add(len(text))
                missed.add(len(text))
            elif texinput and c == FALSE_HYPHEN:
                false.add(len(text))
            elif texinput and c in DIGITS:
                weights[len(text)] = int(c)
            else:
                text.append(c)
                weights[len(text)] = default_weight
        return "".join(text).lower(), hyphens, missed, false, weights

    def compute_margins(self):
        mleft = 1000
        mright = 1000
        for word, hyphen in self.d_hyphens.items():
            if hyphen:
                mleft = min(mleft, min(hyphen))
                mright = min(mright, len(word) - max(hyphen))
        self.margins = (mleft, mright)

    def _chunk(self, word, position, chunklen):
        if position > len(word):
            return
        word = "." + word + "."
        start = max(0, self.margins[0] + 1 - position)
        end = min(len(word) - chunklen, len(word) - self.margins[1] - position)
        for i in range(start, end):
            yield i, word[i:i+chunklen]
        
    def _generate_pattern_statistics(self, patlen, position, inhibiting, training=True):
        good = defaultdict(int)
        bad = defaultdict(int)
        dictionary = self.d_hyphens if training else self.hyphens
        for word, hyphens in dictionary.items():
            missed = self.missed[word]
            false = self.false[word]
            weight = self.d_weights[word]

            for start, ch in self._chunk(word, position, patlen):
                index = start + position - 1
                w = weight[index]
                if not inhibiting:
                    if index in missed:
                        good[ch] += w
                    elif index not in hyphens:
                        bad[ch] += w
                elif index in false:
                    good[ch] += w
                elif index in hyphens and index not in missed:
                    bad[ch] += w
        res = [(ch, good[ch], bad[ch]) for ch in sorted(set(good.keys()) | set(bad.keys()))]
        return res

    def train(self, maxmult=8, false_weight=1, callback=None):
        print(f"Margins: {self.margins}")
        inhibiting = len(self.patterns) & 1
        lastwin = None
        initlist = [0] * (self.maxrange * (maxmult - 1))
        mult_start = 2
        scores = [set() for i in range(maxmult-1)]
        rng = 3
        statsproc = self._multi_stats # if not len(self.patterns) else self._best_stats
        while rng < self.maxrange:
            patterns = {}
            for cluster in range(rng):
                for position in range(rng):
                    for ch, ngood, nbad in self._generate_pattern_statistics(
                                        cluster, position, inhibiting):
                        for mult in range(maxmult-1):
                            score = ngood - nbad * (mult + mult_start)
                            if score < 1 or score > 65535:
                                continue
                            scores[mult].add(score)
                            if ch not in patterns:
                                patterns[ch] = array('H', initlist)
                            index = mult * self.maxrange + position
                            v = patterns[ch][index]
                            if v < score:
                                patterns[ch][index] = score
            # print("pattern length: {}, scores: {}, mult_start: {}".format(len(patterns), list(map(len, scores)), mult_start))
            winners = []
            misseds, falses = statsproc(patterns, rng-1, maxmult-1, scores)
            for mult in range(maxmult-1):
                if not len(misseds[mult]):
                    continue
                bestscore = min((k for k in sorted(misseds[mult].keys(), key=int) if assess(misseds[mult][k], falses[mult][k], inhibiting, false_weight, rng) > 0), key=lambda i:assess(misseds[mult][i], falses[mult][i], inhibiting, false_weight, rng))
                winners.append((assess(misseds[mult][bestscore], falses[mult][bestscore], inhibiting, false_weight, rng),
                                rng, bestscore, mult + mult_start,
                                misseds[mult][bestscore], falses[mult][bestscore]))
            if len(winners):
                winner = min(range(len(winners)), key=lambda w:winners[w][0])
                if lastwin is None or winners[winner][0] < lastwin[0]:
                    lastwin = winners[winner]
                mult_start += max(0, winner-1)
                # print(rng, winner, winners)
                if callback is not None:
                    callback(winner == len(winners) - 1)
                if winner == len(winners) - 1:
                    rng -= 1
                    mult_start += 1
            rng += 1
        if lastwin is None:
            return (0, 0, 0, 0, 0, 0)
        return lastwin

    def train_one(self, rng, mult, score):
        inhibiting = len(self.patterns) & 1
        patterns = defaultdict(set)
        for cluster in range(rng):
            for position in range(rng):
                for ch, ngood, nbad in self._generate_pattern_statistics(
                                    cluster, position, inhibiting, training=False):
                    if ngood - nbad * mult > score:
                        patterns[ch].add(position)
        for word, hyphens in self.hyphens.items():
            prediction = predict(word, patterns, rng, self.maxrange, self.margins)
            if not inhibiting:
                self.missed[word].difference_update(prediction)
                self.false[word].update(prediction - hyphens)
            else:
                self.false[word].difference_update(prediction)
                self.missed[word].update(hyphens & (prediction - self.missed[word]))
        return patterns

    def _best_stats(self, patterns, rng, mult, scores):
        inhibiting = len(self.patterns) & 1
        nmissed = [defaultdict(int) for i in range(mult)]
        nfalse = [defaultdict(int) for i in range(mult)]
        for word, hyphens in self.d_hyphens.items():
            predictions = multi_predict(word, patterns, rng, mult, scores, self.maxrange, self.margins)
            for mult, pred in enumerate(predictions):
                for score, p in pred.items():
                    if not inhibiting:
                        misseds = self.missed[word] - p
                        falses = self.false[word] | (p - hyphens)
                    else:
                        falses = self.false[word] - p
                        misseds = self.missed[word] | (hyphens & (p - self.missed[word]))
                    nmissed[mult][score] += len(misseds)  # sum(self.d_weights[word][j] for j in misseds)
                    nfalse[mult][score] += len(falses)    # sum(self.d_weights[word][j] for j in falses)
        return nmissed, nfalse

    def _multi_stats(self, patterns, rng, mult, scores):
        inhibiting = len(self.patterns) & 1
        nmissed = [defaultdict(int) for i in range(mult)]
        nfalse = [defaultdict(int) for i in range(mult)]
        if not self.multiproc:
            class MyProc:
                pass
            myproc = MyProc()
            def current_process():
                return myproc

        else:
            current_process = multiprocessing.current_process

        def setup(patterns, missed, false, scores, rng, mult, inhibiting, maxrange, margins):
            proc = current_process()
            proc.patterns = patterns
            proc.missed = missed
            proc.false = false
            proc.scores = scores
            proc.rng = rng
            proc.mult = mult
            proc.inhibiting = inhibiting
            proc.maxrange = maxrange
            proc.margins = margins

        setup_parms = [patterns, self.missed, self.false, scores, rng, mult, inhibiting, self.maxrange, self.margins]
        if self.multiproc:
            pool = multiprocessing.Pool(None, setup, setup_parms)
            runmap = pool.imap_unordered
        else:
            setup(*setup_parms)
            def getpool():
                return myproc
            def runmap(fn, items, chunksize=0):
                return [fn(x, getpool=getpool) for x in items]

        for (m, f) in runmap(score_predictions, self.d_hyphens.items(), len(self.d_hyphens) // 64):
            for i in range(mult):
                for k, v in m[i].items():
                    nmissed[i][k] += v
                for k, v in f[i].items():
                    nfalse[i][k] += v
        return nmissed, nfalse

    def _update_stats(self, patterns, rng, mult, score):
        inhibiting = len(self.patterns) & 1
        for word, hyphens in self.d_hyphens.items():
            p = self._multi_predict(word, patterns, rng, mult, [score])[0]
            if not inhibiting:
                self.missed[word].difference_update(p)
                self.false[word].update(p - hyphens)
            else:
                self.false[word].difference_update(p)
                self.missed[word].update(hyphens & (p - self.missed[word]))

    def commit(self, rng, mult, score):
        if rng == 0:
            self.patterns.append(None)
            self.rngs.append((0, 0, 0))
        else:
            pattern = self.train_one(rng, mult, score)
            self.rngs.append((rng, mult, score))
            self.patterns.append(pattern)

    def _allkeys(self):
        keys = set()
        for layer in self.patterns:
            if layer is not None:
                keys.update(layer.keys())
        return keys

    def pattern_strings(self):
        for key in sorted(self._allkeys(), key=lambda s:(-len(s), s)):
            control = self._get_control(key)
            if control:
                yield self._format_pattern(key, control)

    def _get_control(self, key):
        control = {}
        for i, layer in enumerate(self.patterns):
            if layer is None:
                continue
            for index in layer.get(key, EMPTYSET):
                control[index] = i + 1
        return control

    def _format_pattern(self, key, control):
        out = []
        for i in range(len(key) + 1):
            if i > 0:
                out.append(key[i-1])
            c = control.get(i, 0)
            if c > 0:
                out.append(str(c))
        return ''.join(out)

    def hyphenate(self, word):
        prediction = set()
        for i, layer in enumerate(self.patterns):
            if layer is None:
                continue
            rngs = self.rngs[i]
            p = predict(word, layer, rngs[0], self.maxrange, self.margins)
            if i & 1:
                prediction.difference_update(p)
            else:
                prediction.update(p)
        return prediction

    def mismatches(self):
        for word, hyphen in self.hyphens.items():
            prediction = self.hyphenate(word)
            missed = hyphen - prediction
            false = prediction - hyphen
            if missed or false:
                yield word, hyphen, missed, false

    def create_layers(self, false_weight=100, callback=None):
        lastmissed = 2000
        lastfalse = 2000
        for i in range(7):
            (bestres, rng, score, mult, missed, false) = self.train(false_weight=false_weight, callback=callback)
            if bestres == 0:
                break
            print(f"{i+1} {rng}:{mult}>{score} missed: {missed}, false: {false}")
            if missed >= lastmissed and false >= lastfalse:
                print("Skipping commit")
                self.commit(0, 0, 0)
            else:
                self.commit(rng, mult, score)
                lastmissed = missed
                lastfalse = false
            if callback is not None:
                callback()
            if missed == 0 and false == 0:
                break

    def asTeX(self):
        if any(l is not None for l in self.patterns):
            res = ["\\patterns{"]
            patterns = list(self.pattern_strings())
            for i in range(len(patterns) // 10 + 1):
                res.append(" ".join(patterns[i*10:(i+1)*10]))
            res.append("}")
        res.append("\\hyphenation{")
        words = list(self.mismatches())
        res.extend(self.format_dictionary_word(w[0], w[1]) for w in words)
        res.append("}")
        out = "\n".join(res)
        return (out, sum(map(len, patterns)), len(patterns), len(words))

    def format_dictionary_word(self, word, hyphens):
        text = []
        for i in range(len(word) + 1):
            if i > 0:
                text.append(word[i-1].replace(TRUE_HYPHEN, "\u2010"))
            if i in hyphens:
                text.append(TRUE_HYPHEN)
        return "".join(text)


if __name__ == "__main__":
    import sys
    
    p = Patgen()
    p.load_dict(sys.argv[1], samples=20000)
    print(len(p.missed), len(p.d_hyphens))
    p.compute_margins()
    p.create_layers(false_weight=100)
    print(p.rngs)
    output, patlen, numpat, numwords = p.asTeX()
    print("Patterns: {}={:.3f} kB, Words: {}".format(numpat, patlen/1024, numwords))
    print(output)
