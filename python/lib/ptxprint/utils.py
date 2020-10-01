import gettext
import locale
import os, sys
from inspect import currentframe

APP = 'ptxprint'
MODIR = os.path.join(os.path.dirname(__file__), 'mo')

_ = gettext.gettext

def setup_i18n():
    if sys.platform.startswith('win'):
        if os.getenv('LANG') is None:
            lang, enc = locale.getdefaultlocale()
            os.environ['LANG'] = lang
    else:
        locale.bindtextdomain(APP, MODIR)
    locale.setlocale(locale.LC_ALL, '')
    gettext.bindtextdomain(APP, MODIR)

def f_(s):
    frame = currentframe().f_back
    return eval("f'{}'".format(_(s)), frame.f_locals, frame.f_globals)
