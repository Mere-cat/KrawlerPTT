import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup
from time import sleep

def enterBoard(url):
    driver = webdriver.Firefox()
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
    strTime = strTime.split(' ')
    if '' in strTime:
        strTime.remove('')
    monthTab = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    strMonth = strTime[1]
    month = monthTab.index(strMonth) + 1
    day = strTime[2]
    time = strTime[3]
    year = strTime[4]

    resTime = year + '-' + str(month) + '-' + day + ' ' + time
    return resTime.strip()

def getAurIp(allF2):
    for span in allF2:
        span = span.getText().strip()
        if span[0: 5] == "※ 發信站":
            ip = span.split(':')[2]
            ip = ip.split('(')[0]
            return ip.strip()
    return -1

def getPostMetaInfo(soup, postUrl):
   
    ID = getPostId(postUrl)

    strBoard = soup.find('a', class_ = 'board').getText().strip()
    BOARD = getBoard(strBoard)

    allF2 = soup.find_all('span', class_ = 'f2')
    AUTHOR_IP = getAurIp(allF2)

    metaInfo = soup.find_all('span', class_ = 'article-meta-value')
    if (len(metaInfo) != 0):

        AUTHOR = metaInfo[0].getText().strip()

        TITLE = metaInfo[2].getText().strip()

        strTime = metaInfo[len(metaInfo)-1].getText().strip()
        TIME_STAMP = getTime(strTime)
        return [ID, TITLE, AUTHOR, BOARD, TIME_STAMP, AUTHOR_IP]
    
    else: return [ID, -1, -1, BOARD, -1, AUTHOR_IP]

def getPostCont(allCont):
    # Post itself
    contParts = allCont.getText().strip().split('--')
    texts = contParts[0].split('\n')
    contents = texts[1:]
    firstCont = ' '.join(contents)

    # author's reply
    replys = contParts[len(contParts)-1].split('\n')

    # delete comments
    NumComt = 0
    for i in range(len(replys)):
        reply = replys[i]
        if (reply == ''):
            NumComt = NumComt + 1
            continue
        elif (reply[0] == '噓' or reply[0] == '推' or reply[0] == '→' or reply[0] == '※'):
            NumComt = NumComt + 1
            replys[i] = ''
            continue

    for i in range(NumComt):
        replys.remove('')

    # delete footer (if exist)
    if (len(replys) != 0):
        del replys[len(replys)-1]

    # combine post and reply
    secondCont = ' '.join(replys)
    content = firstCont + secondCont
    
    return content.strip()

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