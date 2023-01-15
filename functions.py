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

def getAurIp(ipPart):
    for span in ipPart:
        span = span.getText().strip()
        print(span)
        if span[0: 5] == "※ 發信站":
            ip = span.split(':')[2]
            ip = ip.split('(')[0]
            #return ip.strip()
    return "0.0.0.0"

def getPostMetaInfo(soup, postUrl):
    
    ID = getPostId(postUrl)

    #allF2 = soup.find_all('span', class_ = 'e7-main-content')
    AUTHOR_IP = '---'

    metaInfo = soup.find_all('span', class_ = 'e7-head-content')
    BOARD = metaInfo[0].getText().strip()

    AUTHOR = metaInfo[1].getText().strip()

    strTime = metaInfo[2].getText().strip()
    TIME_STAMP = getTime(strTime)
    
    return [ID, AUTHOR, BOARD, TIME_STAMP, AUTHOR_IP]

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
                print(texts)
                # Concate all
                contParts = contParts + ' ' + texts
    # if we only have one 'e7-main-content' div (allCont), run this:
    else:
        # delete all f3 span first
        for span in allCont.find_all('span', class_ = 'f3'): 
            span.decompose()
        # Find all of the post content 
        contPara = allCont.find_all('span', class_ = '')
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

    # The author ip information
    # The author ip is in the last 'f3' class span
    ipPart = allCont[0].find_all('span', class_ = 'f3')
    AUTHOR_IP = getAurIp(ipPart) # extract the ip address from all of the 'f3' span tags

    return [CONTENT,AUTHOR_IP]

def getComt(allCont):
    pushes = allCont.find_all('div', class_ = 'push')
    comts = []
    comters = []
    ratings = []

    allCnt = len(pushes)
    booCnt = 0
    neturalCnt = 0
    pushCnt = 0

    for push in pushes:
        rating = push.find('span', class_ = 'push-tag').getText().strip()
        ratings.append(rating)
        if(rating == '推'): pushCnt += 1
        elif(rating == '噓'): booCnt += 1
        else: neturalCnt += 1

        comter = push.find('span', class_ = 'push-userid').getText().strip()
        comters.append(comter)

        comt = push.find('span', class_ = 'push-content').getText().strip()
        comt = comt[2:]
        comts.append(comt)

    # list to string
    comts = '!@#'.join(comts)
    ratings = '!@#'.join(ratings)
    comters = '!@#'.join(comters)

    # calculate polarity
    count = pushCnt - booCnt
    polarity = {
        "all": allCnt,
        "boo": booCnt,
        "count": count,
        "neutral": neturalCnt,
        "push": pushCnt
    }

    return [comts, ratings, comters, polarity]