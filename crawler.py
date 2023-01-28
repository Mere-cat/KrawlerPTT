"""
This program will execute the crawling work, using the functions
written in 'functions.py.'
-----------------------------------------------------------------

In this program, we run a nested loop to do the crawling. 

The outer loop will grab the html elements in the content page, 
and scroll down the current window each iteration. The html 
elements we grab is the post list in the content page.

Once we have grabbed the post list in one iteration of the outer 
loop, we'll enter the inner loop. 
In each iteration of the inner loop, we enter one post page from
the post list, and crawl the information we need, such as post title,
post author, post content, etc. In the end of the inner loop, we'll
append the information from the current post to our data set.

The last part of this program, is to output the whole data set as 
a .csv file.
"""
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import functions as myFun # The functions to get the information
import default_var as DFLT # some of our default setting

def crawl(board, totalPost, dataSet):

    url = 'https://www.pttweb.cc/bbs/' + board

    # Check if web page exists.
    # If the HTTP status code is 200, our request succeed.
    rsp = requests.get(url).status_code
    if(rsp != 200): return -1

    # Enter the index page
    # The enterBoard() function will open a new tab and go to the 'url' using selenium
    driverIdx = myFun.enterBoard(url);

    # Count the number of posts we crawled
    postCnt = 0

    # The loop to scroll the window
    for i in range(0, DFLT.MAX_SCROLLING):

        # End the loop: we obtained the given number of data
        if (postCnt == totalPost):
            break

        # Get the elements in this page
        soupIdx = myFun.BeautifulSoup(driverIdx.page_source, 'html.parser') # obtain all the html elements in this page, stored as soupIdx
        posts = soupIdx.find_all('div', class_='e7-right-top-container e7-no-outline-all-descendants') # In the soupIdx, extract divs with the specific class (represents each post)

        # Remove style and script tag from soupIdx
        for tag in soupIdx():
            for attribute in ["script", "style"]:
                del tag[attribute]
        
        # Enter each post page
        for post in posts:
            # Set the default valuse for TITLE, AUTHOR and TIME_STAMP
            TITLE = 'no title'
            AUTHOR = 'NULL'
            TIME_STAMP = 'no record'

            # End the loop: we obtained the given number of data
            if (postCnt == totalPost):
                break

            # Crawl the info from each post
            if post.find('span', class_='e7-title').getText().strip()[0: 8] != '(本文已被刪除)':
                # We obtain post TITLE from the index page
                TITLE = post.find('span', class_='e7-title')
                TITLE = TITLE.find('span', class_='e7-show-if-device-is-not-xs').getText().strip()
                
                # Check if the post has already been crawled:
                # Since we may re-crawl the top post, we'll check if this post has already crawled
                # before crawling it. The top post may in the top 5 rows in our data set, thus we only
                # check for the first five rows.
                for headPost in range(0, 5):
                    # Data in our data set is less then 5
                    if(len(dataSet) < 5): continue
                    # If we find the post been crawled, we'll break the loop and move to next post
                    if(TITLE in dataSet[headPost]):
                        break

                # Enter each article
                postCnt = postCnt + 1
                linkElement = post.find('a', class_ = 'e7-article-default') # get the post link element
                #postUrl = 'https://www.pttweb.cc/bbs/Gossiping/M.1673716679.A.DE4' # testing url
                postUrl = 'https://www.pttweb.cc' + linkElement['href'] # get the 'href' part
                driverEachPost = myFun.enterBoard(postUrl) # enter the post
                soupEachPost = myFun.BeautifulSoup(driverEachPost.page_source, 'html.parser') # get the elements in this page

                # Wait until we load all of the image
                myFun.time.sleep(1)  

                # If there exists a 'load more' btn
                btn = soupEachPost.find_all('button', class_='amber--text v-btn v-btn--outline v-btn--depressed theme--dark')
                if(btn):
                    btn = driverEachPost.find_element(By.CSS_SELECTOR,'button.amber--text')
                    # Click it
                    driverEachPost.execute_script("arguments[0].click();", btn)
                    # Scroll down to bottom
                    driverEachPost.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    # apply beautifulSoup again
                    soupEachPost = myFun.BeautifulSoup(driverEachPost.page_source, 'html.parser')              
                
                # Obtain post meta info: ID, AUTHOR, BOARD, TIME_STAMP, RATING and POLARITY
                metaInfo = myFun.getPostMetaInfo(soupEachPost, postUrl)
                ID = metaInfo[0]
                if(metaInfo[1] != -1):
                    AUTHOR = metaInfo[1]
                BOARD = metaInfo[2]
                if(metaInfo[3] != -1):
                    TIME_STAMP = metaInfo[3]
                RATING = metaInfo[4]
                POLARITY = metaInfo[5]

                # Obtain AUTHOR_IP
                allf3 = soupEachPost.find_all('span', class_ = 'f3')
                AUTHOR_IP = myFun.getAurIp(allf3)

                # Obtain IMG_SRC
                image = soupEachPost.find_all('img', itemprop = 'image')
                IMG_SRC = myFun.getImgSrc(image)

                # Obtain CONTENT
                # notice this will decompose all of the f3 span in allCont
                allCont = soupEachPost.find_all('div', class_ = 'e7-main-content')
                CONTENT = myFun.getPostCont(allCont)

                # Obtain the comments part: COMMENTS, RATING, COMMENTERS, POLARITY
                allCommt = soupEachPost.find_all('div', itemprop = 'comment')
                COMMENTS = myFun.getCommt(allCommt)
                COMMENTERS = myFun.getCommter(allCommt)

                # Close the driver for the post page
                driverEachPost.quit()

                # Write data into data set
                eachData = [ID, TITLE, AUTHOR, BOARD, CONTENT, TIME_STAMP, AUTHOR_IP, COMMENTS, RATING, COMMENTERS, POLARITY, IMG_SRC]
                dataSet.append(eachData)


        # Scroll down to bottom
        driverIdx.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        myFun.time.sleep(DFLT.SCROLL_PAUSE_TIME)            

    # Close the driver for the index page            
    driverIdx.quit()

    # Output the data
    df = myFun.pd.DataFrame(dataSet)
    df.columns = ["ID", "TITLE", "AUTHOR", "BOARD", "CONTENT", "TIME_STAMP", "AUTHOR_IP", "COMMENTS", "RATING", "COMMENTERS", "POLARITY", "IMG_SRC"]
    df.to_csv("output.csv")

    return 0