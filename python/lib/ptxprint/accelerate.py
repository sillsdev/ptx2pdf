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
    processLine(buffer, r"\+.*?(-\d)", r"-1")

def removeUntilNum(buffer, *a): # ^1 ^2 ... ^8 ^9
    num = str(a[0][0])
    processLine(buffer, r"\+.*([+-]+\d+\[{})".format(num), r"\1")

def duplicateLine(buffer, *a): # ^d
    line_start_iter, line_end_iter = getCurrentLineIters(buffer)
    line_text = buffer.get_text(line_start_iter, line_end_iter, True)
    buffer.insert(line_end_iter, line_text)

def shrinkText(buffer, *a): # ^d
    print("Hit Ctrl-minus")
    # Question for MH: How can we get & set this value of this control?
    # Do we need to pass in the model?
    # set("s_viewEditFontSize", get("s_viewEditFontSize") - 1)
    
def growText(buffer, *a): # ^d
    print("Hit Ctrl-plus")
    # set("s_viewEditFontSize", get("s_viewEditFontSize") + 1)

def moveLines(buffer, *a):
    # Check if text is selected
    selected_text = ""
    if buffer.get_has_selection():
        start_iter, end_iter = buffer.get_selection_bounds()
        buffer.cut_clipboard(Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD), True)
        cursor_iter = buffer.get_iter_at_mark(buffer.get_insert())
    else:
        line_start_iter, line_end_iter = getCurrentLineIters(buffer)
        selected_text = buffer.get_text(line_start_iter, line_end_iter, True)
        buffer.delete(line_start_iter, line_end_iter)
        cursor_iter = buffer.get_iter_at_mark(buffer.get_insert())
        while not cursor_iter.starts_line():
            cursor_iter.backward_char()
        
    if a[0][0]:  # down = True; up = False
        cursor_iter.forward_line()
    else:
        cursor_iter.backward_line()
    
    buffer.place_cursor(cursor_iter)
    if selected_text == "":
        buffer.paste_clipboard(Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD), None, True)
    else:
        buffer.insert(cursor_iter, selected_text)
    # Question for MH: Why does the cursor end up 2 lines further on after doing a Down operation?
    
    # This bit doesn't work at all yet
    # Restore the selection
    if buffer.get_has_selection():
        start_iter = buffer.get_iter_at_mark(buffer.get_selection_bound())
        end_iter = buffer.get_iter_at_mark(buffer.get_insert())
        buffer.select_range(start_iter, end_iter)
        
# Each dict within the list represents a different tab on the View+Edit page
bindings = [
    # Front Matter
    {Gdk.KEY_d:     (duplicateLine, ),
     Gdk.KEY_Up:    (moveLines, False),
     Gdk.KEY_Down:  (moveLines, True),
     Gdk.KEY_minus: (shrinkText, ),
     Gdk.KEY_equal: (growText, ),
     Gdk.KEY_l:     (removeLine, )},
    # AdjList
    {Gdk.KEY_1:     (justPlusOne, ),
     Gdk.KEY_2:     (removeUntilNum, 2),
     Gdk.KEY_3:     (removeUntilNum, 3),
     Gdk.KEY_4:     (removeUntilNum, 4),
     Gdk.KEY_5:     (removeUntilNum, 5),
     Gdk.KEY_6:     (removeUntilNum, 6),
     Gdk.KEY_7:     (removeUntilNum, 7),
     Gdk.KEY_8:     (removeUntilNum, 8),
     Gdk.KEY_9:     (removeUntilNum, 9),
     Gdk.KEY_grave: (shrinkLine, ),
     Gdk.KEY_i:     (shrinkLine, ),
     Gdk.KEY_d:     (duplicateLine, ),
     Gdk.KEY_l:     (removeLine, )},
    # Final SFM
    {Gdk.KEY_minus: (shrinkText, ),
     Gdk.KEY_equal: (growText, )},
    # tex file
    {Gdk.KEY_minus: (shrinkText, ),
     Gdk.KEY_equal: (growText, )},
    # tex log
    {Gdk.KEY_minus: (shrinkText, ),
     Gdk.KEY_equal: (growText, )},
    # General Editing tab(1)
    {Gdk.KEY_d:     (duplicateLine, ),
     Gdk.KEY_Up:    (moveLines, False),
     Gdk.KEY_Down:  (moveLines, True),
     Gdk.KEY_minus: (shrinkText, ),
     Gdk.KEY_equal: (growText, ),
     Gdk.KEY_l:     (removeLine, )},
    # General Editing tab(2)
    {Gdk.KEY_d:     (duplicateLine, ),
     Gdk.KEY_Up:    (moveLines, False),
     Gdk.KEY_Down:  (moveLines, True),
     Gdk.KEY_minus: (shrinkText, ),
     Gdk.KEY_equal: (growText, ),
     Gdk.KEY_l:     (removeLine, )},
    ]

