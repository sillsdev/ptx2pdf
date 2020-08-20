"""
The STY stylesheet file parser module.

This defines the database schema for STY files necessary to drive the SFM DB
parser and pre-processing to remove comments, etc.
"""
__author__ = "Tim Eves"
__date__ = "06 January 2020"
__copyright__ = "Copyright © 2020 SIL International"
__license__ = "MIT"
__email__ = "tim_eves@sil.org"
# History:
# 09-Nov-2010 tse   Update to use unique field type's set object and fix poor
#                   quality error messages that fail to identify the source
#                   file.
# 26-Jan-2010 tse   Rewrote to use new palaso.sfm.records module.
# 11-Jan-2010 tse   Initial version.

import re

from . import records
import warnings
from collections import abc
from .records import sequence, unique, level
from .records import UnrecoverableError


_comment = re.compile(r'\s*#.*$')
_markers = re.compile(r'^\s*\\[^\s\\]+\s')


def _munge_records(rs):
    yield from ((r.pop('Marker').lstrip(), r) for r in rs)


class marker(dict):
    def __init__(self, iterable=(), **kwarg):
        self.update(iterable)
        self.update(kwarg)

    def __getitem__(self, key):
        return super().__getitem__(key.casefold())

    def __setitem__(self, key, value):
        return super().__setitem__(key.casefold(), value)

    def __delitem__(self, key):
        return super().__delitem__(key.casefold())

    def __contains__(self, key):
        return super().__contains__(key.casefold())

    def copy(self):
        return marker(self)

    def get(self, key, *args, **kwds):
        return super().get(key.casefold(), *args, **kwds)

    def pop(self, key, *args, **kwargs):
        return super().pop(key.casefold(), *args, **kwargs)

    def setdefault(self, key, *args, **kwargs):
        super().setdefault(key, *args, **kwargs)

    def update(self, iterable=(), **kwarg):
        if isinstance(iterable, abc.Mapping):
            iterable = iterable.items()
        super().update({k.casefold(): v for k, v in iterable})
        super().update({k.casefold(): v for k, v in kwarg.items()})


_fields = marker({
    'Marker': (str, UnrecoverableError(
                        'Start of record marker: {0} missing')),
    'Endmarker':      (str, None),
    'Name':            (str,   None),
    'Description':     (str,   None),
    'OccursUnder':     (unique(sequence(str)), {None}),
    # 'Rank':            (int,   None),
    'TextProperties':  (unique(sequence(str)), {}),
    'TextType':        (str,   'Unspecified'),
    'StyleType':       (str,   None),
    # 'FontSize':        (int,   None),
    # 'Regular':         (flag,  False),
    # 'Bold':            (flag,  False),
    # 'Italic':          (flag,  False),
    # 'Underline':       (flag,  False),
    # 'Superscript':     (flag,  False),
    # 'Smallcaps':       (flag,  False),
    # 'Justification':   (str,   'Left'),
    # 'SpaceBefore':     (int,   0),
    # 'SpaceAfter':      (int,   0),
    # 'FirstLineIndent': (float, 0),
    # 'LeftMargin':      (float, 0),
    # 'RightMargin':     (float, 0),
    # 'Color':           (int,   0),
})


def parse(source, error_level=level.Content):
    '''
    >>> from pprint import pprint
    >>> r = parse(r"""
    ... \\Marker toc1
    ... \\Name toc1 - File - Long Table of Contents Text
    ... \\Description Long table of contents text
    ... \\OccursUnder h h1 h2 h3
    ... \\Rank 1
    ... \\TextType Other
    ... \\TextProperties paragraph publishable vernacular
    ... \\StyleType Paragraph
    ... \\FontSize 12
    ... \\Italic
    ... \\Bold
    ... \\Color 16384""".splitlines(True))
    >>> pprint((r, 
    ...         sorted(r['toc1']['OccursUnder']),
    ...         sorted(r['toc1']['TextProperties'])))
    ... # doctest: +ELLIPSIS
    ({'toc1': {'bold': '',
               'color': '16384',
               'description': 'Long table of contents text',
               'endmarker': None,
               'fontsize': '12',
               'italic': '',
               'name': 'toc1 - File - Long Table of Contents Text',
               'occursunder': {...},
               'rank': '1',
               'styletype': 'Paragraph',
               'textproperties': {...},
               'texttype': 'Other'}},
     ['h', 'h1', 'h2', 'h3'],
     ['paragraph', 'publishable', 'vernacular'])
    >>> r = parse(r"""
    ... \\Marker dummy1
    ... \\Name dummy1 - File - dummy marker definition
    ... \\Description A marker used for demos
    ... \\OccursUnder id NEST
    ... \\TextType Other
    ... \\Bold
    ... \\Color 12345""".splitlines(True))
    >>> pprint((sorted(r.items()),
    ...         sorted(r['dummy1']['OccursUnder'])))
    ... # doctest: +ELLIPSIS
    ([('dummy1',
       {'bold': '',
        'color': '12345',
        'description': 'A marker used for demos',
        'endmarker': None,
        'name': 'dummy1 - File - dummy marker definition',
        'occursunder': {...},
        'styletype': None,
        'textproperties': {},
        'texttype': 'Other'})],
     ['NEST', 'id'])
    ''' # noqa

    # strip comments out
    no_comments = (_comment.sub('', l) for l in source)

    with warnings.catch_warnings():
        warnings.simplefilter(
            "always" if error_level > level.Content else "ignore")
        rec_parser = records.parser(
                        no_comments,
                        records.schema('Marker', _fields),
                        error_level=error_level)
        rec_parser.source = getattr(source, 'name', '<string>')
        recs = iter(rec_parser)
        next(recs, None)
        res = dict(_munge_records(recs))
    _reify(res)
    return res


def _reify(sheet):
    for r in sheet.values():
        for f, v in r.items():
            if isinstance(v, records.sfm.text):
                r[f] = str(v)


def update_sheet(sheet, ammendments={}, **kwds):
    """
    Merge update an existing sheet with records from a supplied dictionary and
    any keyword arguments as well. Only non defaulted fields for each record
    in ammendments or keyword args will overrite the fields in any marker
    records with matching marker names.
    This updated sheet is also returned.

    sheet: The sheet to be updated.
    ammendments: A Mapping from marker names to marker records continaing
        the fields to be updated.
    **kwds: marker id keywords assigned to marker records continaing
        the fields to be updated.
    >>> from pprint import pprint
    >>> base = parse(r'''
    ...              \\Marker test
    ...              \\Name test - A test'''.splitlines(True))
    >>> pprint(base)
    {'test': {'description': None,
              'endmarker': None,
              'name': 'test - A test',
              'occursunder': {None},
              'styletype': None,
              'textproperties': {},
              'texttype': 'Unspecified'}}
    >>> pprint(update_sheet(base,
    ...        test={'OccursUnder': {'p'}, 'FontSize': '12'},
    ...        test2={'Name': 'test2 - new marker'}))
    {'test': {'description': None,
              'endmarker': None,
              'fontsize': '12',
              'name': 'test - A test',
              'occursunder': {'p'},
              'styletype': None,
              'textproperties': {},
              'texttype': 'Unspecified'},
     'test2': {'Name': 'test2 - new marker'}}
    >>> update = parse(r'''
    ...                \\Marker test
    ...                \\Name test - A test
    ...                \\TextType Note'''.splitlines(True))
    >>> pprint(update)
    {'test': {'description': None,
              'endmarker': None,
              'name': 'test - A test',
              'occursunder': {None},
              'styletype': None,
              'textproperties': {},
              'texttype': 'Note'}}
    >>> pprint(update_sheet(base, update))
    {'test': {'description': None,
              'endmarker': None,
              'fontsize': '12',
              'name': 'test - A test',
              'occursunder': {'p'},
              'styletype': None,
              'textproperties': {},
              'texttype': 'Note'},
     'test2': {'Name': 'test2 - new marker'}}
    """
    ammendments.update(**kwds)
    for marker, new_meta in ammendments.items():
        try:
            meta = sheet[marker]
            meta.update(
                fv for fv in new_meta.items()
                if fv[0] not in _fields or fv[1] != _fields[fv[0]][1])
        except KeyError:
            sheet[marker] = new_meta

    return sheet
