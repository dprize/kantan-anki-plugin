# -*- coding: utf-8 -*-
# Copyright: Derick Prize <derickprize.github.io>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

import urllib
from BeautifulSoup import BeautifulSoup
from aqt import mw

def _encode(word):
	return urllib.quote(word.encode('utf-8', ''))

def getJapaneseDefinition(word):
    global urllib
    global _encode
    url = "http://dic.yahoo.co.jp/detail?p=" + _encode(word) + "&stype=0&dtype=0"
    source = urllib.urlopen(url).read()
    soup = BeautifulSoup(source)
    result = soup.find('table', attrs={'class':'d-detail'}).getText()
    return result

def getEnglishDefinition(word):
	global urllib
	global BeautifulSoup
	url = "http://tangorin.com/general/" + _encode(word)
	# url = "http://tangorin.com/general/" + word
	source = urllib.urlopen(url).read()
	soup = BeautifulSoup(source)
	result = soup.find('span', attrs={'class':'eng'})
	if result == None:
		return ""
	else:
		return result.getText()

# returns an image url for "word" using yahoo images
def getImage(word):
	global urllib
	url = "http://images.search.yahoo.com/search/images;_ylt=A0WTb_nizItLfGoAC_eJzbkF?p=" + _encode(word)
	source = urllib.urlopen(url).read()
	soup = BeautifulSoup(source)
	result = soup.find('li', attrs={'class':'ld', 'data-bns':'API.YAlgo'}).contents[0].contents[0]['src']
	(filename, headers) = urllib.urlretrieve(result)
	name = mw.col.media.addFile(filename)
	return name

# useful helpers to add the final result
def addJapaneseDefinition(words):
    finalResult = ""
    wordsLength = len(words)

    for index, word in enumerate(words):
        finalResult += word + ": "
        finalResult += getJapaneseDefinition(word)
        if (index != (wordsLength - 1)): # don't want spaces at the end.
            finalResult += "<br><br>"

    return finalResult

def addEnglishDefinition(words):
    finalResult = ""
    wordsLength = len(words)

    for index, word in enumerate(words):
        finalResult += word + ": "
        finalResult += getEnglishDefinition(word)
        if (index != (wordsLength - 1)): # don't want spaces at the end.
            finalResult += "<br><br>"

    return finalResult

def addImage(words):
    finalResult = ""
    wordsLength = len(words)

    for index, word in enumerate(words):
        finalResult += word + ": "
        # call function dynamically and grab any english or japanese definition.
        finalResult += "<img src=\"" + getImage(word) + "\">"
        if (index != (wordsLength - 1)): # don't want spaces at the end.
            finalResult += "<br><br>"
    return finalResult