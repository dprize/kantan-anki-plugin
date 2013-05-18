# -*- coding: utf-8 -*-
# Copyright: Derick Prize <derickprize.github.io>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

# button on the editor to add english definitions

from aqt import mw
from aqt.editor import Editor
from anki.hooks import wrap
from BeautifulSoup import BeautifulSoup
import definition
from aqt.utils import showText

srcField = 'Expression'
engDstField = 'EnglishMeaning'

def toggleEnglishDefinition(self):
    n = self.note
    if "japanese" not in n.model()['name'].lower():
        return False
    srcTxt = mw.col.media.strip(n[srcField])
    if not srcTxt:
        return False
    soup = BeautifulSoup(srcTxt)
    result = soup.findAll('b')
    wordList = []
    for r in result:
        wordList.append(r.contents[0])
    n[engDstField] = definition.addEnglishDefinition(wordList)
    self.loadNote()
    self.loadNote() # if I don't call loadNote twice, the content of n['Meaning'] will dissapear. Bug?
    return True

def setupButtons(self):
    self._addButton("mybutton", lambda s=self: toggleEnglishDefinition(self),
        text=u"英", tip="Add english definition (Ctrl+e)", key="Ctrl+e")

Editor.toggleEnglishDefinition = toggleEnglishDefinition
Editor.setupButtons = wrap(Editor.setupButtons, setupButtons)
