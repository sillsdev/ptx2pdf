import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

def onTextEditKeypress(widget, event, bufView):
    print(onTextEditKeypress)
    i, buffer, view = bufView
    
    state = event.state
    keyval = event.keyval
    print(f"{i=} {state=}")
    if state == Gdk.ModifierType.CONTROL_MASK:
        print(f"{keyval=}  {bindings[i]=}")
        if i < len(bindings) and keyval in bindings[i]:
            info = bindings[i][keyval]
            info[0](buffer, info[1:])

def duplicateLine(buffer, *a):
    print("duplicateLine")
    insert_iter = buffer.get_iter_at_mark(buffer.get_insert())
    line_start_iter = insert_iter.copy()
    line_end_iter = insert_iter.copy()

    if line_start_iter.starts_line():
        line_start_iter.backward_line()
    else:
        line_start_iter.set_line_offset(0)

    if not line_end_iter.ends_line():
        line_end_iter.forward_to_line_end()

    line_text = buffer.get_text(line_start_iter, line_end_iter, True)
    buffer.insert(insert_iter, line_text + '\n')

def removeLine(buffer, *a):
    print("removeLine")
    insert_iter = buffer.get_iter_at_mark(buffer.get_insert())
    line_start_iter = insert_iter.copy()
    line_end_iter = insert_iter.copy()

    if line_start_iter.starts_line():
        line_start_iter.backward_line()
    else:
        line_start_iter.set_line_offset(0)

    if not line_end_iter.ends_line():
        line_end_iter.forward_to_line_end()

    buffer.delete(line_start_iter, line_end_iter)

def removeUntilNum(buffer, *a):
    start_iter, end_iter = buffer.get_bounds()
    line_text = buffer.get_text(start_iter, end_iter, True)
    new_line_text = line_text.replace('+0', '+1', 1)
    buffer.set_text(new_line_text)

def shrinkLine(buffer, *a):
    cursor_iter = buffer.get_iter_at_mark(buffer.get_insert())
    match_iter = cursor_iter.forward_search(r'\[2\]', Gtk.TextSearchFlags.VISIBLE_ONLY, None)
    if match_iter:
        match_start, match_end = match_iter
        start, _ = buffer.get_bounds()
        buffer.delete(start, match_end)

bindings = [
    {Gdk.KEY_1: (removeUntilNum, 1)},
    {Gdk.KEY_2: (removeUntilNum, 2)},
    {Gdk.KEY_3: (removeUntilNum, 3)},
    {Gdk.KEY_4: (removeUntilNum, 4)},
    {Gdk.KEY_5: (removeUntilNum, 5)},
    {Gdk.KEY_6: (removeUntilNum, 6)},
    {Gdk.KEY_i: (shrinkLine, )},
    {Gdk.KEY_d: (duplicateLine, )},
    {Gdk.KEY_l: (removeLine, )},
    ]

