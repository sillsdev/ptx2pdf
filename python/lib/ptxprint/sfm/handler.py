'''
The original callback based SFM parser API implemented ontop of the new SFM 
parser system.
'''
__version__ = '20101011'
__date__    = '11 October 2010'
__author__  = 'Tim Eves <tim_eves@sil.org>'
__history__ = '''
	20101026 - tse - rewrote to use new palaso.sfm module
'''
import ptxprint.sfm as sfm
import warnings



class handler(object):
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
        if isinstance(e, basestring): 
            return line + handler.text(e.pos, e.parent, e)
        
        line += u'\\' + handler.start(e.pos, e.parent and e.parent.name, e.name, e.args)
        body = reduce(_g, e, u'')
        line += body if not body or not body.startswith('\\\\') and body.startswith(('\r\n','\n','\\')) else u' ' + body
        tag = handler.end(e.pos, e.parent and e.parent.name, e.name)
        if tag: line += u'\\' + tag
        return line
    
    
    with warnings.catch_warnings():
        warnings.showwarning = handler.error
        warnings.resetwarnings()
        warnings.simplefilter("always", SyntaxWarning)
        
        doc = parser(source)
        return reduce(_g, doc, u'').splitlines(True)



def parse(parser,handler,source):
    def _g(_, e):
        if isinstance(e, basestring): 
            handler.text(e.pos, e.parent, e)
        else:
            handler.start(e.pos, e.parent.name, e.name, e.args)
            reduce(_g, e, u'')
            handler.end(e.pos, e.parent.name, e.name)
    
    
    with warnings.catch_warnings():
        warnings.showwarning = handler.error
        warnings.resetwarnings()
        warnings.simplefilter("always", SyntaxWarning)
        
        doc = parser(source)
        return reduce(_g, doc, u'').splitlines(True)



if __name__ == '__main__':
    import ptxprint.sfm.usfm as usfm
    import sys, codecs
    mat=codecs.open(sys.argv[1],'rb',encoding='utf-8_sig')
    out=codecs.open(sys.argv[2],'wb',encoding='utf-8',buffering=1)
    out.writelines(transduce(usfm.parser, sfm.handler(), mat))

