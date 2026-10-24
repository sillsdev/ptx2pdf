#!/usr/bin/env python3
# Rebuilds locales/ptxprint.pot without needing an xgettext that understands Glade (the MSYS2 build does not).
# Does what the Makefile's locales/ptxprint.pot rule does, minus the Crowdin upload:
#   perl ... ptxprint.glade > temp.glade      (makes name="name" properties translatable)
#   xgettext -k_ --from-code=utf-8 lib/ptxprint/*.py temp.glade
# Python strings come from xgettext; Glade strings are read with an XML parser (same references,
# "temp.glade:<line>"); msgcat merges them in the same order and layout as xgettext would.
#
#   python makePot.py            # writes locales/ptxprint.pot
#   python makePot.py --out x.pot --bin C:/msys64/usr/bin
import argparse
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
from xml.parsers import expat

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from poLib import Entry, writePo      # noqa: E402

pythonDir = os.path.dirname(os.path.dirname(here))


def gladeEntries(path):
    """(text, line, comment) for every translatable element, in document order."""
    with open(path, encoding='utf-8') as f:
        data = f.read()
    # the Makefile's perl one-liner
    data = re.sub(r'(name="name")', r'\1 translatable="yes"', data)
    out = []
    stack = []
    p = expat.ParserCreate()
    p.buffer_text = True

    def start(tag, attrs):
        stack.append({'translatable': attrs.get('translatable') == 'yes', 'line': p.CurrentLineNumber,
                      'comment': attrs.get('comments', ''), 'text': ''})

    def chars(t):
        if stack:
            stack[-1]['text'] += t

    def end(tag):
        e = stack.pop()
        if e['translatable'] and e['text']:
            out.append((e['text'], e['line'], e['comment']))

    p.StartElementHandler, p.CharacterDataHandler, p.EndElementHandler = start, chars, end
    p.Parse(data.encode('utf-8'), True)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', default=os.path.join(pythonDir, 'locales', 'ptxprint.pot'))
    ap.add_argument('--bin', default='', help="folder holding xgettext and msgcat if they are not on PATH")
    args = ap.parse_args()
    env = dict(os.environ)
    if args.bin:
        env['PATH'] = args.bin + os.pathsep + env['PATH']
    tmp = tempfile.mkdtemp()
    xgettext = shutil.which('xgettext', path=env['PATH']) or sys.exit('xgettext not found (use --bin)')
    msgcat = shutil.which('msgcat', path=env['PATH']) or sys.exit('msgcat not found (use --bin)')
    pyPot, gladePot = os.path.join(tmp, 'py.pot'), os.path.join(tmp, 'glade.pot')

    pyFiles = sorted('lib/ptxprint/' + os.path.basename(f)                    # relative, like the Makefile
                     for f in glob.glob(os.path.join(pythonDir, 'lib', 'ptxprint', '*.py')))
    subprocess.run([xgettext, '-k_', '--from-code=utf-8', '-L', 'Python', '-o', pyPot] + pyFiles,
                   cwd=pythonDir, env=env, check=True)

    byId = {}
    order = []
    for text, line, comment in gladeEntries(os.path.join(pythonDir, 'lib', 'ptxprint', 'ptxprint.glade')):
        e = byId.get(text)
        if e is None:
            e = byId[text] = Entry()
            e.msgid = text
            order.append(e)
        e.refs.append('temp.glade:{}'.format(line))
        if comment and ('#. ' + comment) not in e.comments:
            e.comments.append('#. ' + comment)
    head = Entry()
    head.msgstr = "Content-Type: text/plain; charset=UTF-8\n"
    writePo(gladePot, [head] + order)

    # --use-first keeps xgettext's header and merges references of identical msgids
    subprocess.run([msgcat, '--use-first', '-o', args.out, pyPot, gladePot], env=env, check=True)
    print("wrote", args.out)


if __name__ == '__main__':
    main()
