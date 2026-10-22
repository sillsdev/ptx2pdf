#!/usr/bin/python3

# Regression tests for copying a style's settings into a new style (issue #789)

import os
from ptxprint.styleditor import StyleEditor

basesty = os.path.join(os.path.dirname(__file__), "..", "src", "ptx2pdf.sty")
src = "cat:box|esb"

class MockModel:
    def changed(self):
        pass
    def getFont(self, *a, **k):
        return None

def makeEditor():
    se = StyleEditor(MockModel(), basepath=basesty)
    se.sheet = {}
    se.marker = src
    return se

def addCopy(se, key):
    se.addMarker(key, key)
    se.copyMarkerValues(src, key)
    return se.sheet[key]

def test_copyBaseOnlyStyle():
    ''' A stock style that only exists in the base stylesheet must still be copied '''
    se = makeEditor()
    assert src not in se.sheet
    new = addCopy(se, "cat:copy|esb")
    assert new['border'] == 'All'
    assert new['position'] == 'p'

def test_copyKeysWithoutWidgets():
    ''' Border and padding settings have no widget in the style editor, but must be copied '''
    se = makeEditor()
    se.sheet[src] = {'borderwidth': '0.2', 'bordervpadding': '0', 'boxhpadding': '8',
                     'bordercolor': '0.00 0.00 0.00', 'fontsize': '10'}
    new = addCopy(se, "cat:copy|esb")
    for k, v in se.sheet[src].items():
        assert new[k] == v
    assert new['border'] == 'All'       # from the base sheet, under the user's overrides

def test_copyDoesNotCopyIdentity():
    ''' What identifies a style is set from the dialog, so is not copied from the source '''
    se = makeEditor()
    se.sheet[src] = {'name': 'original', ' category': 'Other', 'description': 'orig desc',
                     'endmarker': 'x*', 'mrktype': 'internal', 'styletype': 'Paragraph',
                     'texttype': 'Other', 'borderwidth': '0.2'}
    new = addCopy(se, "cat:copy|esb")
    assert new['name'] == "cat:copy|esb"
    assert new[' deletable'] is True
    assert ' category' not in new
    for k in StyleEditor.identityKeys:
        assert k not in new or k == 'name'
    assert new['borderwidth'] == '0.2'
    assert se.sheet[src]['name'] == 'original'

def test_copyAddsNothingExtra():
    ''' The copy has exactly the source's effective formatting, plus the new name '''
    se = makeEditor()
    se.sheet[src] = {'border': 'Bottom Right', 'borderwidth': '10'}
    new = addCopy(se, "cat:copy|esb")
    expected = {k: v for k, v in se.asStyle(src).items() if k != 'name'}
    assert {k: v for k, v in new.items() if k not in ('name', ' deletable')} == expected
