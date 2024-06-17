import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import re
import logging

logger = logging.getLogger(__name__)

def onTextEditKeypress(widget, event, bufView):
    i, buffer, view, model = bufView
    logger.debug(f"KeyPress {event.keyval} in {event.state} in buffer {i}")
    state = event.state
    keyval = event.keyval
    if (state & Gdk.ModifierType.CONTROL_MASK) != 0:
        if i < len(bindings) and keyval in bindings[i]:
            info = bindings[i][keyval]
            info[0](buffer, view, model, info[1:])

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

def removeLine(buffer, view, model, *a): # ^l
    line_start_iter, line_end_iter = getCurrentLineIters(buffer)
    buffer.delete(line_start_iter, line_end_iter)

def commentOut(buffer, view, model, *a): # ^/
    cmt = a[0][0]
    line_start_iter, line_end_iter = getCurrentLineIters(buffer)
    line_text = buffer.get_text(line_start_iter, line_end_iter, True)
    if line_text.startswith(cmt):
        new_line_text = line_text[len(cmt):].lstrip()
    else:
        new_line_text = cmt + " " + line_text
    buffer.delete(line_start_iter, line_end_iter)
    buffer.insert(line_start_iter, new_line_text)

def justPlusOne(buffer, view, model, *a): # ^1
    processLine(buffer, r"\+(\d)", lambda m:"+" + ("1" if m.group(1) == "0" else "0"))

def shrinkLine(buffer, view, model, *a): # ^i
    processLine(buffer, r"\+.*?(-\d)", r"+-1")

def removeUntilNum(buffer, view, model, *a): # ^1 ^2 ... ^8 ^9
    num = str(a[0][0])
    processLine(buffer, r"\+.*([+-]+\d+\[{})".format(num), r"\1")

def duplicateLine(buffer, view, model, *a): # ^d
    line_start_iter, line_end_iter = getCurrentLineIters(buffer)
    line_text = buffer.get_text(line_start_iter, line_end_iter, True)
    buffer.insert(line_end_iter, line_text)

def shrinkText(buffer, view, model, *a): # ^minus
    model.set("s_viewEditFontSize", str(float(model.get("s_viewEditFontSize")) - 1))
    model.setEntryBoxFont()

    
def growText(buffer, view, model, *a): # ^plus (actually ^equal as shift isn't held)
    model.set("s_viewEditFontSize", str(float(model.get("s_viewEditFontSize")) + 1))
    model.setEntryBoxFont()

def moveLines(buffer, view, model, *a): # ^Up or ^Down
    if buffer.get_has_selection():
        start_iter, end_iter = buffer.get_selection_bounds()
        selected_text = buffer.get_text(start_iter, end_iter, True)
        buffer.delete(start_iter, end_iter)
        cursor_iter = buffer.get_iter_at_mark(buffer.get_insert())
    else:
        line_start_iter, line_end_iter = getCurrentLineIters(buffer)
        selected_text = buffer.get_text(line_start_iter, line_end_iter, True)
        buffer.delete(line_start_iter, line_end_iter)
        cursor_iter = buffer.get_iter_at_mark(buffer.get_insert())
        while not cursor_iter.starts_line():
            cursor_iter.backward_char()
        
    if a[0][0]:  # True when Down, False when Up
        cursor_iter.forward_line()
    else:
        cursor_iter.backward_line()
    
    buffer.insert(cursor_iter, selected_text)

    if a[0][0]:  # True when Down, False when Up
        cursor_iter.backward_line()
        cursor_iter.backward_line()
    
    buffer.place_cursor(cursor_iter)

def count_selected_lines(buffer):
    start_iter, end_iter = buffer.get_selection_bounds()
    selected_text = buffer.get_text(start_iter, end_iter, include_hidden_chars=False)
    num_lines = selected_text.count('\n')
    if selected_text and selected_text[-1] != '\n':
        num_lines += 1
    return num_lines

# Each dict within the list represents a different tab on the View+Edit page
bindings = [
    # Front Matter
    {Gdk.KEY_0:     (commentOut, r"\rem"),
     Gdk.KEY_comma: (commentOut, r"\rem"),
     Gdk.KEY_d:     (duplicateLine, ),
     Gdk.KEY_Up:    (moveLines, False),
     Gdk.KEY_Down:  (moveLines, True),
     Gdk.KEY_minus: (shrinkText, ),
     Gdk.KEY_equal: (growText, ),
     Gdk.KEY_l:     (removeLine, )},
    # AdjList
    {Gdk.KEY_0:     (commentOut, r"%"),
     Gdk.KEY_comma: (commentOut, r"%"),
     Gdk.KEY_1:     (justPlusOne, ),
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
    # log file
    {Gdk.KEY_minus: (shrinkText, ),
     Gdk.KEY_equal: (growText, )},
    # General Editing tab(1)
    {Gdk.KEY_0:     (commentOut, r"#"),
     Gdk.KEY_comma: (commentOut, r"%"),
     Gdk.KEY_d:     (duplicateLine, ),
     Gdk.KEY_Up:    (moveLines, False),
     Gdk.KEY_Down:  (moveLines, True),
     Gdk.KEY_minus: (shrinkText, ),
     Gdk.KEY_equal: (growText, ),
     Gdk.KEY_l:     (removeLine, )},
    # General Editing tab(2)
    {Gdk.KEY_0:     (commentOut, r"#"),
     Gdk.KEY_comma: (commentOut, r"%"),
     Gdk.KEY_d:     (duplicateLine, ),
     Gdk.KEY_Up:    (moveLines, False),
     Gdk.KEY_Down:  (moveLines, True),
     Gdk.KEY_minus: (shrinkText, ),
     Gdk.KEY_equal: (growText, ),
     Gdk.KEY_l:     (removeLine, )},
    ]

