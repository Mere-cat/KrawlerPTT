import time
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

from bs4 import BeautifulSoup
from time import sleep

def enterBoard(url):
    # make selenium not pop up windows
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)

    driver.get(url)
    driver.add_cookie({"name": "over18", "value": "1"})
    driver.get(url)
    return driver

def getPostId(postUrl):
    urlParts = postUrl.split('/')
    numParts = len(urlParts)
    ID = urlParts[numParts-1]
    ID = ID.replace(".html", "")
    return ID

def getBoard(strBoard):
    strBoard = strBoard.split(' ')
    return strBoard[1]

def getTime(strTime):
    strTime = strTime.replace('(', ')')
    strTime = strTime.split(')')
    return strTime[1]

def getAurIp(allf3):
    # The author ip information
    # The author ip is in the last 'f3' class span
    for span in allf3:
        tmp = span.getText().strip()
        
        # get the first "發信站"
        if tmp[0: 5] == "※ 發信站":
            ip = tmp.split(':')[2]
            ip = ip.split('※')[0]

            # remove the country information
            # if the last character in ip is ')', it implies the ip contains the country name
            if(ip[-1] == ')'):
                ip = ip.split('(')[0]
            return ip
    return "0.0.0.0"

def getCommt(allCommt):
    commts = []
    for i in range(0, len(allCommt)):
        #print(i)
        commt = allCommt[i].find_all('div', itemprop = 'text')[0].getText()
        #print(commt)
        commts.append(commt)

    if len(commts) > 0:
        COMMENTS = '!@#'.join(commts)
        return COMMENTS
    else: return "no comment"

def getCommter(allCommt):
    commters = []
    for i in range(0, len(allCommt)):
        commter = allCommt[i].find_all('div', itemprop = 'author')[0].getText()
        commters.append(commter)

    if len(commters) > 0:
        COMMENTER = '!@#'.join(commters)
        return COMMENTER
    else: return "no commenter"

def getPostMetaInfo(soup, postUrl):
    
    ID = getPostId(postUrl)

    metaInfo = soup.find_all('span', class_ = 'e7-head-content')
    BOARD = metaInfo[0].getText().strip()

    AUTHOR = metaInfo[1].getText().strip()

    strTime = metaInfo[2].getText().strip()
    TIME_STAMP = getTime(strTime)

    ratings = metaInfo[3].getText().strip()
    RATING = ratings.split('(')[0]

    # Polarity
    polarities = ratings.split('(')[1]
    polarities = polarities.split(' ')

    pushCnt = int(polarities[0].strip('推'))
    booCnt = int(polarities[1].strip('噓'))
    neturalCnt = int(polarities[2].strip('→)'))
    allCnt = pushCnt + booCnt + neturalCnt

    POLARITY = {
        "all": allCnt,
        "boo": booCnt,
        "count": int(RATING),
        "neutral": neturalCnt,
        "push": pushCnt
    }
    
    return [ID, AUTHOR, BOARD, TIME_STAMP, RATING, POLARITY]

def getPostCont(allCont):
    # Post itself 
    # The post content itself is in the first element of allCont, inside the span tag with class ''
    contParts = ''
    if len(allCont) > 1: # to see if we have more than one 'e7-main-content' div
        for i in range(0, len(allCont)):
            # delete all f3 span first
            for span in allCont[i].find_all('span', class_ = 'f3'): 
                span.decompose()
            # Find all of the post content in the current 'e7-main-content' div
            contPara = allCont[i].find_all('span', class_ = '')
            # If we can find any '' span in the current 'e7-main-content' div
            for j in range(0, len(contPara)):
                # Replace new line with space
                texts = contPara[j].getText().strip().strip('--').replace('\n', ' ')
                # Concate all
                contParts = contParts + ' ' + texts

    # if we only have one 'e7-main-content' div (allCont), run this:
    else:
        # delete all f3 span first
        for span in allCont[0].find_all('span', class_ = 'f3'): 
            span.decompose()
        # Find all of the post content 
        contPara = allCont[0].find_all('span', class_ = '')
        for j in range(0, len(contPara)):
            # Replace new line with space
            texts = contPara[j].getText().strip('--').strip().replace('\n', ' ')
            # Concate all
            contParts = contParts + ' ' + texts

    contPara = allCont[0].find('span', class_ = '')
    for i in range(0, len(contPara)-1):
        # Replace new line with space
        texts = contPara[j].getText().strip('--').strip().replace('\n', ' ')
        # Concate all
        contParts = contParts + ' ' + texts

    # author's reply
    replys = ''
    flag = 0 # flag is 0 if
    for i in range(1, len(allCont)):
        if(allCont[i].find('span', class_ = "")):
            replys = replys + ' ' + allCont[i].find('span', class_ = "").getText().strip()
            flag = 1

    if(flag == 1):
        CONTENT = contParts + replys
    else:
        CONTENT = contParts

    return CONTENT