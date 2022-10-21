#!/usr/bin/python
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the University nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

# Py2 and Py3 compatibility
from builtins import chr
import unicodedata
import re

try: unicode
except NameError:
    unicode = str

hexescre = re.compile(r"(?:\\(?:ux)\{([0-9a-fA-F]+)\}|\\u([0-9a-fA-F]{4})|\\U([0-9a-fA-F]{8})|\\x([0-9a-fA-F]{2}))")
hexgre = re.compile(r"\\u\{([0-9a-fA-F]+)\}")
simpleescs = {
    'a' : u"\u0007",
    'b' : u"\u0008",
    't' : u"\u0009",
    'n' : u"\u000A",
    'v' : u"\u000B",
    'f' : u"\u000C",
    'r' : u"\u000D",
    '\\' : u"\u005C"
}
simpleescsre = re.compile(r"\\([^0-9])")
groupsre = re.compile(r"\\([0-9]+)")


def us2list(text):
    """Convert a string of Unicode Sets into a list of strings."""
    res = parse(text)
    if len(res) > 0:
        return res[0]
    else:
        return list()


def list2us(list_of_strings, ucd):
    """Convert a list of strings to a string of Unicode Sets.

    The strings must be in NFC.
    """
    unicode_set = list()
    for text in list_of_strings:
        braces_needed = _need_braces(text)
        text = _escape_us_syntax(text)
        text = _hex_escape(text, ucd)
        if braces_needed:
            text = _add_needed_braces(text)
        unicode_set.append(text)
    return u'[{}]'.format(' '.join(unicode_set))


def _need_braces(text):
    """Determine if braces will be needed."""
    if len(text) > 1:
        return True
    return False


def _add_needed_braces(text):
    """Add braces."""
    return u'{' + text + u'}'


def _hex_escape(text, ucd):
    """Escape marks if they are isolated (that is, with no base character)."""
    modified_text = ''
    is_isolated = True
    for char in text:
        if ucd.need_hex_escape(char, is_isolated):
            char = _escape_using_hex(char)
        if char == ' ':
            is_isolated = True
        else:
            is_isolated = False
        modified_text += char
    return modified_text


def _escape_us_syntax(text):
    """Escape characters used in Unicode Set syntax."""
    modified_text = ''
    for char in text:
        char = _escape_using_backslash(char)
        modified_text += char
    return modified_text


def _escape_using_hex(char):
    """Use hex digits to escape the character."""
    codepoint = ord(char)
    if codepoint > 0xFFFF:
        return u'\\U{:08x}'.format(codepoint)
    return u'\\u{:04x}'.format(codepoint)


def _escape_using_backslash(s):
    """Use a backslash to escape the character."""
    return escapechar(s)
    ###return "\\" + s if s in '[]{}\\' else s


def escapechar(s):
    return u"\\"+ s if s in '[]{}\\&-|^$:' else s


class UnicodeSetSequence(list):

    def __init__(self, *p, **kw):
        super(list, self).__init__(*p, **kw)
        self.groups = []

    def reverse(self):
        new = UnicodeSetSequence(self)
        l = len(self)
        new.groups = [(l-x[0], l-x[1]) for x in self.groups]
        return new


class UnicodeSet(set):
    '''A UnicodeSet is a simple set of characters also a negative attribute'''
    def __init__(self, *a, **kw):
        super(UnicodeSet, self).__init__(*a, **kw)
        self.negative = False
        self.isclass = False
        self.startgroup = False
        self.endgroup = False

    def asSet(self):
        """ Returns a set of strings, one per 'character' in the flattened set. """
        if self.negative:
            return set()
        res = set()
        for s in self:
            if isinstance(s, UnicodeSet):
                res.update(s.asSet())
            else:
                res.add(s)
        return res

    def negate(self, state):
        self.negative = state

    def setclass(self, state):
        self.isclass = state


def _expand(p, vals, ind, indval):
    if vals[ind][indval].startswith("\\"):
        g = p.group(int(vals[ind][indval][1]))
        return "".join(_expand(p, vals, i, indices[i]) for i in range(g[0], g[1]))
    else:
        return vals[ind][indval]


def flatten(s, normal=None):
    p = parse(s, normal=normal)
    vals = list(map(sorted, p))
    lens = list(map(len, vals))
    num = len(vals)
    indices = [0] * num
    while True:
        for i in range(num):
            if indices[i] == lens[i] - 1:
                indices[i] = 0
            else:
                indices[i] += 1
                break
        else:
            return
        res = []
        yield u"".join(_expand(p, vals, i, x) for i, x in enumerate(indices))


def struni(s, groups=None):
    s = hexescre.sub(lambda m:escapechar(chr(int(m.group(m.lastindex), 16))), s)
    s = simpleescsre.sub(lambda m:simpleescs.get(m.group(1), m.group(1)), s)
    if groups is not None:
        s = groupsre.sub(lambda m:groups[int(m.group(1)) - 1], s)
    return s


def parse(s, normal=None):
    '''Returns a sequence of UnicodeSet'''
    # convert escapes
    s = hexescre.sub(lambda m:escapechar(chr(int(m.group(m.lastindex), 16))), s)
    # don't flatten \\ escapes here since we need to differentiate with action chars {}[]
    s = hexgre.sub(lambda m:"{"+u"".join(escapechar(chr(int(x, 16))) for x in m.group(1).split())+"}", s)
    s = s.replace(' ', '')
    res = UnicodeSetSequence()
    i = 0
    currgroup = -1
    while i < len(s):
        (i, item, nextitem) = parseitem(s, i, None, len(s))
        # a sequence can't have binary operators in it
        if nextitem.startgroup:
            currgroup = len(res)
        elif nextitem.endgroup:
            res.groups.append((currgroup, len(res)))
        if len(nextitem):
            res.append(nextitem)
    if normal is not None:
        res = [UnicodeSet(set(unicodedata.normalize(normal, unicode(c)) for c in x)) for x in res]
    return res


def parseitem(s, ind, lastitem, end, usegroups=False):
    '''Parses a single UnicodeSet or character. Doesn't handle property sets or variables, yet.'''
    if ind == end:
        return (end, lastitem, None)
    res = UnicodeSet()
    if s[ind] == '[':
        ind += 1
        if s[ind] == '^':
            res.negate(True)
            ind += 1
        item = None
        res.setclass(True)
        e = s.index(']', ind)
        while e > 0 and s[e-1] == '\\':
            e = s.index(']', e+1)
        while ind < e:
            (ind, item, nextitem) = parseitem(s, ind, item, e)
            if item:
                res.update(item)
            item = nextitem
        if item:
            res.update(item)
        ind += 1
    elif s[ind] in '|&-':
        op = s[ind]
        ind += 1
        if lastitem is None:        # treat as char
            res.add(op)
        else:
            (ind, _, item) = parseitem(s, ind, None, end)
            if op == '|' and lastitem and item:
                if lastitem.negative:
                    if item.negative:
                        res = lastitem & item
                    else:
                        res = lastitem - item
                elif item.negative:
                    res = item - lastitem
                    res.negate(True)
                else:
                    res = item.union(lastitem)
                lastitem = None
            elif op == '&' and lastitem and item:
                if lastitem.negative:
                    if item.negative:
                        res = item.union(lastitem)
                    else:
                        res = item - lastitem
                elif item.negative:
                    res = lastitem - item
                else:
                    res = item & lastitem
                lastitem = None
            elif op == '-':
                # set difference
                if lastitem and item and lastitem.isclass and item.isclass:
                    if lastitem.negative:
                        if item.negative:
                            res = item - lastitem
                        else:
                            res = lastitem | item
                    elif item.negative:
                        res = lastitem & item
                    else:
                        res = lastitem - item
                    lastitem = None
                # char range
                elif lastitem and item and len(lastitem) == 1 and len(item) == 1:
                    for x in range(ord(lastitem.pop()), ord(item.pop())):
                        res.add(chr(x))
                    lastitem = None
                else:
                    res.add(u"-")
            else:
                res.add(op)
    elif s[ind] == '{':
        e = s.index('}', ind+1)
        while e > 0 and s[e-1] == '\\':
            e = s.index('}', e+1)
        res.add(simpleescsre.sub(lambda m:simpleescs.get(m.group(1), m.group(1)), s[ind+1:e]))
        ind = e + 1
    elif s[ind] == '\\':
        x = s[ind+1]
        try:
            y = int(x)
            res.add(u"\\"+x)
        except:
            res.add(simpleescs.get(x, x))
        ind += 2
    elif usegroups and s[ind] == '(':
        res.startgroup = True
        ind += 1
    elif usegroups and s[ind] == ')':
        res.endgroup = True
        ind += 1
    else:
        res.add(s[ind])
        ind += 1
    return (ind, lastitem, res)
