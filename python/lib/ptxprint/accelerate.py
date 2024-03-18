import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import re

def onTextEditKeypress(widget, event, bufView):
    i, buffer, view = bufView
    
    state = event.state
    keyval = event.keyval
    if state == Gdk.ModifierType.CONTROL_MASK:
        if i < len(bindings) and keyval in bindings[i]:
            info = bindings[i][keyval]
            info[0](buffer, info[1:])

def getCurrentLineIters(buffer):
    insert_iter = buffer.get_iter_at_mark(buffer.get_insert())
    line_start_iter = insert_iter.copy()
    line_end_iter = insert_iter.copy()
    if not line_start_iter.starts_line():
        line_start_iter.set_line_offset(0)
    if not line_end_iter.ends_line():
        line_end_iter.forward_to_line_end()
    line_end_iter.forward_char()
    return line_start_iter, line_end_iter

def processLine(buffer, reg, replace):
    line_start_iter, line_end_iter = getCurrentLineIters(buffer)
    line_text = buffer.get_text(line_start_iter, line_end_iter, True)
    new_line_text = re.sub(reg, replace, line_text)
    buffer.delete(line_start_iter, line_end_iter)
    buffer.insert(line_start_iter, new_line_text)

def removeLine(buffer, *a): # ^l
    line_start_iter, line_end_iter = getCurrentLineIters(buffer)
    buffer.delete(line_start_iter, line_end_iter)

def justPlusOne(buffer, *a): # ^1
    processLine(buffer, r"\+0", "+1")

def shrinkLine(buffer, *a): # ^i
    # processLine(buffer, r"\+.*?(-\d+\[)", r"\1")
    processLine(buffer, r"\+.*?(-\d)", r"-1")

def removeUntilNum(buffer, *a): # ^1 ^2 ... ^8 ^9
    num = str(a[0][0])
    processLine(buffer, r"\+.*([+-]+\d+\[{})".format(num), r"\1")

def duplicateLine(buffer, *a): # ^d
    line_start_iter, line_end_iter = getCurrentLineIters(buffer)
    line_text = buffer.get_text(line_start_iter, line_end_iter, True)
    buffer.insert(line_end_iter, line_text)

# Each dict within the list represents a different tab on the View+Edit page
# Common shortcuts: 
#    Ctrl-d = Duplicate Line
#    Ctrl-l = Delete Line
bindings = [
    {Gdk.KEY_d: (duplicateLine, ),
     Gdk.KEY_l: (removeLine, )},
    {Gdk.KEY_1: (justPlusOne, ),
     Gdk.KEY_2: (removeUntilNum, 2),
     Gdk.KEY_3: (removeUntilNum, 3),
     Gdk.KEY_4: (removeUntilNum, 4),
     Gdk.KEY_5: (removeUntilNum, 5),
     Gdk.KEY_6: (removeUntilNum, 6),
     Gdk.KEY_7: (removeUntilNum, 7),
     Gdk.KEY_8: (removeUntilNum, 8),
     Gdk.KEY_9: (removeUntilNum, 9),
     Gdk.KEY_i: (shrinkLine, ),
     Gdk.KEY_d: (duplicateLine, ),
     Gdk.KEY_l: (removeLine, )},
    {},
    {},
    {},
    {Gdk.KEY_d: (duplicateLine, ),
     Gdk.KEY_l: (removeLine, )},
    {Gdk.KEY_d: (duplicateLine, ),
     Gdk.KEY_l: (removeLine, )},
    ]

