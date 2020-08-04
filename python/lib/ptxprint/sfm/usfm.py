'''
The USFM parser module, provides the default sytlesheet for USFM and
USFM specific textype parsers to the palaso.sfm module.  These guide the 
palaso.sfm parser to so it can correctly parser USFM document structure.
'''
__version__ = '20101011'
__date__    = '11 October 2010'
__author__  = 'Tim Eves <tim_eves@sil.org>'
__history__ = '''
	20081210 - djd - Seperated SFM definitions from the module
		to allow for parsing other kinds of SFM models
		Also changed the name to parse_sfm.py as the
		module is more generalized now
	20091026 - tse - renamed and refactored generatoion of markers
		dict to module import time as part of import into palaso 
		package.
	20101026 - tse - rewrote to enable the parser to use the stylesheets to 
		direct how to parse structure and USFM specific semantics.
	20101109 - tse - Ensure cached usfm.sty is upto date after package code 
		changes.
'''
import bz2, contextlib, operator, os, re, site
import pickle
import ptxprint.sfm.style as style
import ptxprint.sfm as sfm
from ptxprint.sfm import level
from itertools import chain
from functools import partial, reduce

_PALASO_DATA = os.path.join(
        os.path.expanduser(os.path.dirname(os.path.normpath(site.USER_SITE))),
        'palaso-python','sfm')



def _check_paths(pred, paths):
    return next(filter(pred, map(os.path.normpath, paths)),None)

def _newer(cache, benchmark):
    return os.path.getmtime(benchmark) <= os.path.getmtime(cache)

def _is_fresh(cached_path, benchmarks):
    return reduce(operator.and_, 
                  map(partial(_newer, cached_path), benchmarks))

def _load_cached_stylesheet(path):
    package_dir = os.path.dirname(__file__)
    source_path = _check_paths(os.path.exists, 
        [ os.path.join(_PALASO_DATA, path),
          os.path.join(package_dir, path)])
    
    cached_path = os.path.normpath(os.path.join(
                        _PALASO_DATA,
                        path+os.extsep+'cz'))
    if os.path.exists(cached_path):
        import glob
        if _is_fresh(cached_path, [source_path] 
                + glob.glob(os.path.join(package_dir, '*.py'))):
            try:
                try:
                    with contextlib.closing(bz2.BZ2File(cached_path,'rb')) as sf:
                        return pickle.load(sf)
                except:
                    os.unlink(cached_path)
            except:
                cached_path = None
    path = os.path.dirname(cached_path)
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except:
            cached_path = None

    res = style.parse(open(source_path,'r',encoding="utf-8"))
    if cached_path:
        import pickletools
        try:
            with contextlib.closing(bz2.BZ2File(cached_path, 'wb')) as zf:
                zf.write(pickletools.optimize(
                    pickle.dumps(res)))
        except:
            return res
    return res


default_stylesheet=_load_cached_stylesheet('usfm.sty')



_default_meta = {'TextType':'Milestone', 'OccursUnder':None, 'Endmarker':None, 'StyleType':None}



class parser(sfm.parser):
    '''
    >>> from pprint import pprint
    >>> import warnings
    
    Tests for inline markers
    >>> list(parser([r'\\test']))
    [element('test')]
    >>> list(parser([r'\\test text']))
    [element('test'), text(' text')]
    >>> list(parser([r'\\id JHN\\ior text\\ior*']))
    [element('id', content=[text('JHN'), element('ior', content=[text('text')])])]
    >>> list(parser([r'\\id MAT\\mt Text \\f + \\fk deep\\fk*\\f*more text.']))
    [element('id', content=[text('MAT'), element('mt', content=[text('Text '), element('f', args=['+'], content=[element('fk', content=[text('deep')])]), text('more text.')])])]

    Test end marker recognition when it's a prefix
    >>> with warnings.catch_warnings():
    ...     warnings.simplefilter("error")
    ...     list(parser([r'\\id TEST\\mt \\f + text\\f*suffixed text']))
    ...     list(parser([r'\\id TEST\\mt \\f + \\fr ref \\ft text\\f*suffixed text']))
    [element('id', content=[text('TEST'), element('mt', content=[element('f', args=['+'], content=[text('text')]), text('suffixed text')])])]
    [element('id', content=[text('TEST'), element('mt', content=[element('f', args=['+'], content=[element('fr', content=[text('ref ')]), text('text')]), text('suffixed text')])])]
    
    Test marker parameters, particularly chapter and verse markers
    >>> list(parser([r'\\id TEST'         r'\\c 1']))
    [element('id', content=[text('TEST'), element('c', args=['1'])])]
    >>> list(parser([r'\\id TEST'         r'\\c 2 \\s text']))
    [element('id', content=[text('TEST'), element('c', args=['2'], content=[element('s', content=[text('text')])])])]
    >>> list(parser([r'\\id TEST\\c 0\\p' r'\\v 1']))
    [element('id', content=[text('TEST'), element('c', args=['0'], content=[element('p', content=[element('v', args=['1'])])])])]
    >>> list(parser([r'\\id TEST\\c 0\\p' r'\\v 1-3']))
    [element('id', content=[text('TEST'), element('c', args=['0'], content=[element('p', content=[element('v', args=['1-3'])])])])]
    >>> list(parser([r'\\id TEST\\c 0\\p' r'\\v 2 text']))
    [element('id', content=[text('TEST'), element('c', args=['0'], content=[element('p', content=[element('v', args=['2']), text('text')])])])]
    >>> list(parser([r'\\id TEST'         r'\\c 2 \\p \\v 3 text\\v 4 verse']))
    [element('id', content=[text('TEST'), element('c', args=['2'], content=[element('p', content=[element('v', args=['3']), text('text'), element('v', args=['4']), text('verse')])])])]

    Test for error detection and reporting for structure
    >>> list(parser([r'\\id TEST\\mt text\\f*']))
    Traceback (most recent call last):
    ... 
    SyntaxError: <string>: line 1,17: orphan end marker \\f*: no matching opening marker \\f
    >>> list(parser([r'\\id TEST     \\p 1 text']))
    Traceback (most recent call last):
    ... 
    SyntaxError: <string>: line 1,14: orphan marker \\p: may only occur under \\c
    >>> list(parser([r'\\id TEST\\mt \\f + text\\fe*']))
    Traceback (most recent call last):
    ... 
    SyntaxError: <string>: line 1,22: orphan end marker \\fe*: no matching opening marker \\fe
    >>> list(parser([r'\\id TEST\\mt \\f + text'], ))
    Traceback (most recent call last):
    ... 
    SyntaxError: <string>: line 1,1: invalid end marker end-of-file: \\f (line 1,13) can only be closed with \\f*

    Test for error detection and reporting for USFM specific parses
    Chapter numbers
    >>> list(parser(['\\id TEST\\c\\p \\v 1 text']))
    Traceback (most recent call last):
    ... 
    SyntaxError: <string>: line 1,9: missing chapter number after \\c
    >>> list(parser(['\\id TEST\\c A\\p \\v 1 text']))
    Traceback (most recent call last):
    ... 
    SyntaxError: <string>: line 1,9: missing chapter number after \\c
    >>> list(parser([r'\\id TEST\\c 1 text\\p \\v 1 text']))
    Traceback (most recent call last):
    ... 
    SyntaxError: <string>: line 1,14: text cannot follow chapter marker '\\c 1'
    >>> list(parser([r'\\id TEST\\c 1text\\p \\v 1 text']))
    Traceback (most recent call last):
    ... 
    SyntaxError: <string>: line 1,13: missing space after chapter number '1'
    
    Verse numbers
    >>> list(parser([r'\\id TEST\\c 1\\p \\v \\p text']))
    Traceback (most recent call last):
    ... 
    SyntaxError: <string>: line 1,16: missing verse number after \\v
    >>> list(parser([r'\\id TEST\\c 1\\p \\v text']))
    Traceback (most recent call last):
    ... 
    SyntaxError: <string>: line 1,16: missing verse number after \\v
    >>> list(parser([r'\\id TEST\\c 1\\p \\v 1text']))
    Traceback (most recent call last):
    ... 
    SyntaxError: <string>: line 1,20: missing space after verse number '1'
    
    Note text parsing
    >>> list(parser([r'\\id TEST\\mt \\f \\fk key\\fk* text.\\f*']))
    Traceback (most recent call last):
    ... 
    SyntaxError: <string>: line 1,13: missing caller parameter after \\f
    >>> list(parser([r'\\id TEST\\mt \\f +text \\fk key\\fk* text.\\f*']))
    Traceback (most recent call last):
    ... 
    SyntaxError: <string>: line 1,17: missing space after caller parameter '+'
    
    Test warnable condition detection and reporting
    >>> with warnings.catch_warnings():
    ...     warnings.simplefilter("error", SyntaxWarning)
    ...     list(parser([r'\\id TEST\\mt \\whoops']))
    Traceback (most recent call last):
    ... 
    SyntaxWarning: <string>: line 1,14: unknown marker \whoops: not in styesheet
    >>> with warnings.catch_warnings():
    ...     warnings.simplefilter("error", SyntaxWarning)
    ...     list(parser([r'\\id TEST\\mt \\whoops'], error_level=sfm.level.Marker))
    Traceback (most recent call last):
    ...
    SyntaxError: <string>: line 1,14: unknown marker \whoops: not in styesheet
    >>> with warnings.catch_warnings():
    ...     warnings.simplefilter("error", SyntaxWarning)
    ...     list(parser([r'\\id TEST\\mt \\zwhoops'], error_level=sfm.level.Note))
    Traceback (most recent call last):
    ... 
    SyntaxWarning: <string>: line 1,14: unknown private marker \zwhoops: not it stylesheet using default marker definition
    '''
    
    default_meta = _default_meta
    numeric_re = re.compile(r'\s*(\d+(:?[-\u2010\2011]\d+)?)',re.UNICODE)
    # paratext has CVregexp as (?:(\d+)[.:]))?(\d+\w?)(?:-(\d+\w?))
    # which handily allows RTL ordering marks as part of \w (but you can't then have \v 12a<RTL>-13 but who wants to?
    verse_re = re.compile(r'\s*(\d+[a-z]?(:?[-,\u200B-\u2011]+\d+[a-z]?)?)',re.UNICODE)
    caller_re = re.compile(r'\s*([^\s\\])',re.UNICODE)
    sep_re = re.compile(r'\s|$',re.UNICODE)
    
    @classmethod
    def extend_stylesheet(cls, *names, **kwds):
        return super(parser,cls).extend_stylesheet(
                kwds.get('stylesheet', default_stylesheet), *names)
    
    
    def __init__(self, source, 
                 stylesheet=default_stylesheet,
                 default_meta=_default_meta, 
                 *args, **kwds):
        if 'purefootnotes' in kwds:
            self.purefootnotes = kwds['purefootnotes']
            del kwds['purefootnotes']
        super().__init__(source, stylesheet, default_meta, private_prefix='z',*args, **kwds)
    
    
    def _force_close(self, parent, tok):
        if tok is not sfm.parser._eos and 'NoteText' in parent.meta.get('TextType',[]):
            self._error(level.Note, 
                'implicit end marker before {token}: \\{0.name} '
                '(line {0.pos.line},{0.pos.col}) '
                'should be closed with \\{1}', tok, parent,
                parent.meta['Endmarker'])
        else: super(parser, self)._force_close(parent, tok)                          
    
    
    def _ChapterNumber_(self, chapter_marker):
        tok = next(self._tokens)
        chapter = self.numeric_re.match(tok)
        if not chapter:
            self._error(level.Content, 'missing chapter number after \\c', 
                                     chapter_marker)
            chapter_marker.args = ['\uFFFD']
        else:
            chapter_marker.args = [str(tok[chapter.start(1):chapter.end(1)])]
            tok = tok[chapter.end():]
        if tok and not self.sep_re.match(tok):
            self._error(level.Content, 'missing space after chapter number \'{chapter}\'',
                                    tok, chapter=chapter_marker.args[0])
        tok  = tok.lstrip()
        if tok:
            if tok[0] == '\\': 
                self._tokens.put_back(tok)
            else:
                self._error(level.Structure, 'text cannot follow chapter marker \'{0}\'', tok, chapter_marker, )
                chapter_marker.append(sfm.element(None, meta=self.default_meta, content=[tok]))
                tok = None
                
        return self._default_(chapter_marker)
    _chapternumber_ = _ChapterNumber_

      
    def _VerseNumber_(self, verse_marker):
        '''
        '''
        tok = next(self._tokens)
        verse = self.verse_re.match(tok)
        if not verse:
            self._error(level.Content, 'missing verse number after \\v', 
                                     verse_marker)
            verse_marker.args = ['\uFFFD']
        else:
            verse_marker.args = [str(tok[verse.start(1):verse.end(1)])]
            tok = tok[verse.end():]
        
        if not self.sep_re.match(tok):
            self._error(level.Content, 'missing space after verse number \'{verse}\'',
                                    tok, verse=verse_marker.args[0])
        tok = tok.lstrip()
        
        if tok: self._tokens.put_back(tok)
        return tuple()
    _versenumber_ = _VerseNumber_
    
    
    @staticmethod
    def _canonicalise_footnote(content):
        def g(e):
            if getattr(e,'name', None) == 'ft':
                e.parent.annotations['content-promoted'] = True
                return e
            else:
                return [e]
        return chain.from_iterable(map(g, content))
    
    
    def _NoteText_(self,parent):
        if parent.meta.get('StyleType') != 'Note': return self._default_(parent)
        
        tok = next(self._tokens)
        caller = self.caller_re.match(tok)
        if not caller:
            self._error(level.Content, 'missing caller parameter after \\{token.name}',
                        parent)
            parent.args = ['\uFFFD']
        else:
            parent.args = [str(tok[caller.start(1):caller.end(1)])]
            tok = tok[caller.end():]
        
        if not self.sep_re.match(tok):
            self._error(level.Content, 'missing space after caller parameter \'{caller}\'',
                                    tok, caller=parent.args[0])
        
        if tok.lstrip(): self._tokens.put_back(tok)

        if self.purefootnotes:
            return self._default_(parent)
        else:
            return self._canonicalise_footnote(self._default_(parent))


    def _Unspecified_(self, parent):
        orig_name = parent.name
        if (parent.meta.get('StyleType') == 'Paragraph' 
           or (parent.parent is not None 
               and parent.parent.meta.get('StyleType') == 'Note' 
               and 'Endmarker' not in parent.meta)):
            parent.name = 'p'
        subparse = self._default_(parent)
        parent.name = orig_name
        return subparse
    _unspecified_ = _Unspecified_



class reference(sfm.position):
    def __new__(cls, pos, ref):
        p = super(reference,cls).__new__(cls, *pos)
        p.book = ref[0]
        p.chapter = ref[1]
        p.verse = ref[2]
        return p


def decorate_references(source):
    ref = [None,None,None]
    def _g(_, e):
        if isinstance(e, sfm.element):
            if   e.name == 'id': ref[0] = str(e[0]).split()[0]
            elif e.name == 'c':  ref[1] = e.args[0]
            elif e.name == 'v':  ref[2] = e.args[0]
            return reduce(_g, e, None)
        e.pos = reference(e.pos, ref)
    source = list(source)
    reduce(_g, source, None)
    return source

