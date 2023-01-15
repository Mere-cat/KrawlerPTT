import requests
from selenium.webdriver.common.by import By
import functions as myFun
import default_var as DFLT

def crawl(board, totalPost, dataSet):

    url = 'https://www.pttweb.cc/bbs/' + board

    # Check if web page exists
    rsp = requests.get(url).status_code
    if(rsp != 200): return -1

    # Enter the index page
    driverIdx = myFun.enterBoard(url);

    # Count the number of posts we crawled
    postCnt = 0

    # The loop to scroll the window
    for i in range(0, DFLT.MAX_SCROLLING):
        # End the loop: we obtained the given number of data
        if (postCnt == totalPost):
            break

        # Get the elements in this page
        soupIdx = myFun.BeautifulSoup(driverIdx.page_source, 'html.parser')
        posts = soupIdx.find_all('div', class_='e7-right-top-container e7-no-outline-all-descendants')

        # Remove style and script
        for tag in soupIdx():
            for attribute in ["script", "style"]:
                del tag[attribute]
        
        # Enter each post
        for post in posts:
            TITLE = 'no title'

            # End the loop
            if (postCnt == totalPost):
                break

            # Crawl the info from each post
            if post.find('span', class_='e7-title').getText().strip()[0: 8] != '(本文已被刪除)':
                #print(postCnt)
                # We obtain post TITLE from the index page, and set default for AUTHOR and TIME_STAMP
                TITLE = post.find('span', class_='e7-title')
                TITLE = TITLE.find('span', class_='e7-show-if-device-is-not-xs').getText().strip()
                reoccured = 0
                
                # If the post has already been crawled
                for headPost in range(0, 5):
                    if(len(dataSet) < 5): continue
                    if(TITLE in dataSet[headPost]):
                        reoccured = 1
                        break

                if (reoccured == 1):
                    reoccured = 0
                    continue

                AUTHOR = 'NULL'
                TIME_STAMP = 'no record'

                # Enter each article
                postCnt = postCnt + 1
                linkElement = post.find('a', class_ = 'e7-article-default')
                #postUrl = 'https://www.pttweb.cc/bbs/Gossiping/M.1673716679.A.DE4' # testing url
                postUrl = 'https://www.pttweb.cc' + linkElement['href']
                driverEachPost = myFun.enterBoard(postUrl)
                soupEachPost = myFun.BeautifulSoup(driverEachPost.page_source, 'html.parser')

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
                #print(allf3)
                AUTHOR_IP = myFun.getAurIp(allf3)

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
                eachData = [ID, TITLE, AUTHOR, BOARD, CONTENT, TIME_STAMP, AUTHOR_IP, COMMENTS, RATING, COMMENTERS, POLARITY]
                dataSet.append(eachData)


        # Scroll down to bottom
        driverIdx.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        myFun.time.sleep(DFLT.SCROLL_PAUSE_TIME)            

    # Close the driver for the index page            
    driverIdx.quit()

    # Output the data
    df = myFun.pd.DataFrame(dataSet)
    df.columns = ["ID", "TITLE", "AUTHOR", "BOARD", "CONTENT", "TIME_STAMP", "AUTHOR_IP", "COMMENTS", "RATING", "COMMENTERS", "POLARITY"]
    df.to_csv("output.csv")

    return 0