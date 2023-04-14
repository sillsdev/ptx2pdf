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

from . import records, ErrorLevel
import warnings
from collections import abc
from .records import sequence, unique
from .records import UnrecoverableError


_comment = re.compile(r'\s*#(?:!|.*$)')
_markers = re.compile(r'^\s*\\[^\s\\]+\s')


def _munge_records(rs):
    yield from ((r.pop('Marker').lstrip(), r) for r in rs)


class CaselessStr(str):
    def __eq__(self, b):
        return self.casefold().__eq__(b.casefold())

    def __hash__(self):
        return self.casefold().__hash__()


class Marker(dict):
    def __init__(self, iterable=(), **kwarg):
        self.update(iterable)
        self.update(kwarg)

    def __getitem__(self, key):
        try:
            return super().__getitem__(key.casefold())
        except KeyError:
            if key in _fields:
                return _fields[key][1]
            raise

    def __setitem__(self, key, value):
        return super().__setitem__(CaselessStr(key), value)

    def __delitem__(self, key):
        return super().__delitem__(key.casefold())

    def __contains__(self, key):
        return super().__contains__(key.casefold())

    def copy(self):
        return Marker(self)

    def get(self, key, *args, **kwds):
        return super().get(key.casefold(), *args, **kwds)

    def pop(self, key, *args, **kwargs):
        return super().pop(key.casefold(), *args, **kwargs)

    def setdefault(self, key, *args, **kwargs):
        super().setdefault(CaselessStr(key), *args, **kwargs)

    def update(self, iterable=(), **kwarg):
        if isinstance(iterable, abc.Mapping):
            iterable = iterable.items()
        super().update({CaselessStr(k): v for k, v in iterable})
        super().update({CaselessStr(k): v for k, v in kwarg.items()})


_fields = Marker({
    'Marker':           (str, UnrecoverableError(
                                'Start of record marker: {0} missing')),
    'Endmarker':        (str, None),
    'Name':             (str,   None),
    'Description':      (str,   None),
    'OccursUnder':      (unique(sequence(str)), set()),
    'TextProperties':   (unique(sequence(CaselessStr)), set()),
    'TextType':         (CaselessStr,   'Unspecified'),
    'StyleType':        (CaselessStr,   ''),
    #'Attributes':       (sequence(str), None)
    # 'Rank':            (int,   None),
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


def old_parse(source, error_level=ErrorLevel.Content, fields=_fields):
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
    ... \\Color 16384
    ... #!\\Attributes attr size ?ref""".splitlines(True))
    >>> pprint((r, 
    ...         sorted(r['toc1']['occursunder']),
    ...         sorted(r['toc1']['textproperties'])))
    ... # doctest: +ELLIPSIS
    ({'toc1': {'Attributes': 'attr size ?ref',
               'Bold': '',
               'Color': '16384',
               'Description': 'Long table of contents text',
               'Endmarker': None,
               'FontSize': '12',
               'Italic': '',
               'Name': 'toc1 - File - Long Table of Contents Text',
               'OccursUnder': {...},
               'Rank': '1',
               'StyleType': 'Paragraph',
               'TextProperties': {...},
               'TextType': 'Other'}},
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
       {'Bold': '',
        'Color': '12345',
        'Description': 'A marker used for demos',
        'Endmarker': None,
        'Name': 'dummy1 - File - dummy marker definition',
        'OccursUnder': {...},
        'StyleType': None,
        'TextProperties': set(),
        'TextType': 'Other'})],
     ['NEST', 'id'])
    ''' # noqa

    # strip comments out
    no_comments = (_comment.sub('', l) for l in source)

    with warnings.catch_warnings():
        warnings.simplefilter(
            "always" if error_level > ErrorLevel.Content else "ignore")
        rec_parser = records.parser(
                        no_comments,
                        records.Schema(
                            'Marker', 
                            type(fields)({CaselessStr(k):v for k,v in fields.items()})),
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
            if isinstance(v, records.sfm.Text):
                r[f] = str(v)


def update_sheet(sheet, ammendments={}, field_replace=False, **kwds):
    """
    Merge update an existing sheet with records from a supplied dictionary and
    any keyword arguments as well. Only non defaulted fields for each record
    in ammendments or keyword args will overrite the fields in any marker
    records with matching marker names. The OccursUnder and TextProperties
    fields of a records are merged by taking the union of new and old, unless
    the field_replace keyword parameter is True
    This updated sheet is also returned.

    sheet: The sheet to be updated.
    ammendments: A Mapping from marker names to marker records continaing
        the fields to be updated.
    field_replace: When True replace OccursUnder and TextProperties.
        When False merge them instead. Defaults to False.
    **kwds: marker id keywords assigned to marker records continaing
        the fields to be updated.
    >>> from pprint import pprint
    >>> base = parse(r'''
    ...              \\Marker test
    ...              \\Name test - A test'''.splitlines(True))
    >>> pprint(base)
    {'test': {'Description': None,
              'Endmarker': None,
              'Name': 'test - A test',
              'OccursUnder': {None},
              'StyleType': None,
              'TextProperties': set(),
              'TextType': 'Unspecified'}}
    >>> pprint(update_sheet(base,
    ...                     test={'OccursUnder': {'p'}, 'FontSize': '12'},
    ...                     test2={'Name': 'test2 - new marker'}))
    ... # doctest: +ELLIPSIS
    {'test': {'Description': None,
              'Endmarker': None,
              'FontSize': '12',
              'Name': 'test - A test',
              'OccursUnder': {...},
              'StyleType': None,
              'TextProperties': set(),
              'TextType': 'Unspecified'},
     'test2': {'Name': 'test2 - new marker'}}
    >>> update = parse(r'''
    ...                \\Marker test
    ...                \\Name test - A test
    ...                \\TextType Note'''.splitlines(True))
    >>> pprint(update)
    {'test': {'Description': None,
              'Endmarker': None,
              'Name': 'test - A test',
              'OccursUnder': {None},
              'StyleType': None,
              'TextProperties': set(),
              'TextType': 'Note'}}
    >>> pprint(update_sheet(base, update))
    ... # doctest: +ELLIPSIS
    {'test': {'Description': None,
              'Endmarker': None,
              'FontSize': '12',
              'Name': 'test - A test',
              'OccursUnder': {...},
              'StyleType': None,
              'TextProperties': set(),
              'TextType': 'Note'},
     'test2': {'Name': 'test2 - new marker'}}
    """
    ammendments.update(**kwds)
    for marker, new_meta in ammendments.items():
        try:
            meta = sheet[marker]
            if not field_replace:
                meta['OccursUnder'] = meta['OccursUnder'].union(new_meta.pop('OccursUnder', set()))
                meta['TextProperties'] = meta['TextProperties'].union(new_meta.pop('TextProperties', set()))
            meta.update(
                fv for fv in new_meta.items()
                if fv[0] not in _fields or fv[1] != _fields[fv[0]][1])
        except KeyError:
            sheet[marker] = new_meta

    return sheet

def simple_parse(source, error_level=ErrorLevel.Content, fields=_fields, categories=False, keyfield="Marker"):
    res = {}
    mkr = ""
    category = ""
    for l in source.readlines():
        m = re.match(r"\\(\S+)\s*(.*)\s*$", l)
        if m is not None:
            key = m.group(1)
            v = m.group(2)
        else:
            continue
        val = fields.get(key, (str, ))[0](v.strip())
        if key.lower() == "category":
            category = val
            key = "Marker"
            val = "esb"
        if key.lower() == keyfield.lower():
            mkr = f"cat:{category}|{val}" if category else val
            res[mkr] = Marker()
        else:
            res[mkr][key] = val
    return res

parse = old_parse

def merge_sty(base, other, forced=False):
    for m, ov in other.items():
        if m not in base or forced:
            base[m] = ov.copy()
        else:
            for k, v in ov.items():
                base[m][k] = v

def out_sty(base, outf, keyfield="Marker"):
    for m, rec in base.items():
        outf.write(f"\n\\{keyfield} {m}\n")
        for k, v in rec.items():
            if isinstance(v, (set, list, tuple)):
                v = " ".join(v)
            outf.write(f"\\{k} {v}\n")

