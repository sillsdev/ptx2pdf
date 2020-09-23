'''
The original callback based SFM parser API implemented ontop of the new SFM
parser system.
'''
__version__ = '20101011'
__date__ = '11 October 2010'
__author__ = 'Tim Eves <tim_eves@sil.org>'
__history__ = '''
    20101026 - tse - rewrote to use new palaso.sfm module
'''
from . import sfm
import warnings
from functools import reduce


class Handler(object):
    def __init__(self):
        self.errors = []

    def start(self, pos, ctag, tag, params):
        return ' '.join([tag]+params)

    def text(self, pos, ctag, text):
        return text

    def end(self, pos, ctag, tag):
        return ''

    def error(self, *warn_msg):
        self.errors.append(warnings.WarningMessage(*warn_msg))


def transduce(parser, handler, source):
    def _g(line, e):
        if isinstance(e, str):
            return line + handler.text(e.pos, e.parent, e)

        line += '\\' + handler.start(e.pos, e.parent and e.parent.name,
                                     e.name, e.args)
        body = reduce(_g, e, '')
        line += body if not body or not body.startswith('\\\\') \
            and body.startswith(('\r\n', '\n', '\\')) else ' ' + body
        tag = handler.end(e.pos, e.parent and e.parent.name, e.name)
        if tag:
            line += f'\\{tag}'
        return line

    with warnings.catch_warnings():
        warnings.showwarning = handler.error
        warnings.resetwarnings()
        warnings.simplefilter("always", SyntaxWarning)

        doc = parser(source)
        return reduce(_g, doc, '').splitlines(True)


def parse(parser, handler, source):
    def _g(_, e):
        if isinstance(e, str):
            handler.text(e.pos, e.parent, e)
        else:
            handler.start(e.pos, e.parent.name, e.name, e.args)
            reduce(_g, e, '')
            handler.end(e.pos, e.parent.name, e.name)

    with warnings.catch_warnings():
        warnings.showwarning = handler.error
        warnings.resetwarnings()
        warnings.simplefilter("always", SyntaxWarning)

        doc = parser(source)
        return reduce(_g, doc, '').splitlines(True)


if __name__ == '__main__':
    import palaso.sfm.usfm as usfm
    import sys
    import codecs

    mat = codecs.open(sys.argv[1], 'rb', encoding='utf-8_sig')
    out = codecs.open(sys.argv[2], 'wb', encoding='utf-8', buffering=1)
    out.writelines(transduce(usfm.parser, sfm.handler(), mat))
