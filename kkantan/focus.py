# -*- coding: utf-8 -*-
# Copyright: Derick Prize <derickprize.github.io>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

# the main code for grabbing definitions when the user is adding cards goes here.
from aqt import mw
from aqt.utils import showText
from anki.hooks import addHook
from BeautifulSoup import BeautifulSoup
import definition

srcField = ['Expression']
jpDstField = ['Meaning']
engDstField = ['EnglishMeaning']
imgDstField = ['Image']

def onFocusLost(flag, n, fidx):
    src = None
    dst = None # japanese destination
    engDst = None
    imgDst = None
    # japanese model?
    if "japanese" not in n.model()['name'].lower():
        return flag
    # have src and dst fields?
    for c, name in enumerate(mw.col.models.fieldNames(n.model())):
        for f in srcField:
            if name == f:
                src = f
                srcIdx = c
        for f in jpDstField:
            if name == f:
                dst = f
        for f in engDstField:
            if name == f:
                engDst = f
        for f in imgDstField:
            if name == f:
                imgDst = f
    if not src or not dst or not engDst or not imgDstField:
        return flag
    # dst field already filled?
    if n[dst]:
        return flag
    # event coming from src field?
    if fidx != srcIdx:
        return flag
    # grab source text
    srcTxt = mw.col.media.strip(n[src])
    if not srcTxt:
        return flag
    # update fields
    try:
        soup = BeautifulSoup(srcTxt)
        result = soup.findAll('b')
        wordList = []

        for r in result:
            wordList.append(r.contents[0])

        n[dst] = definition.addJapaneseDefinition(wordList)
        # add images
        if n[imgDst] == "": # only add a new image if the image destination is empty.
            n[imgDst] = definition.addImage(wordList)

        n.flush()
    except Exception, e:
        raise
    return True
    #definitions  
addHook('editFocusLost', onFocusLost)