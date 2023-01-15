import requests
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
        # End the loop: we obtained the 
        if (postCnt == totalPost):
            break
        
        # Scroll down to bottom
        driverIdx.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
        # Wait to load page
        myFun.time.sleep(DFLT.SCROLL_PAUSE_TIME)

        # Get the elements in this page
        soupIdx = myFun.BeautifulSoup(driverIdx.page_source, 'html.parser')
        posts = soupIdx.find_all('div', class_='e7-right-top-container e7-no-outline-all-descendants')
        #print(len(posts))

        # Remove style and script
        for tag in soupIdx():
            for attribute in ["script", "style"]:
                del tag[attribute]
        
        # Enter each post
        for post in posts:
            # End the loop
            if (postCnt == totalPost):
                break

            # Crawl the info from each post
            if post.find('span', class_='e7-title').getText().strip()[0: 8] != '(本文已被刪除)':
                #print(postCnt)
                # We obtain post TITLE from the index page, and set default for AUTHOR and TIME_STAMP
                TITLE = post.find('span', class_='e7-title')
                TITLE = TITLE.find('span', class_='e7-show-if-device-is-not-xs').getText().strip()
                #print(TITLE)
                AUTHOR = 'NULL'
                TIME_STAMP = 'no record'

                # Enter each article
                postCnt = postCnt + 1
                linkElement = post.find('a', class_ = 'e7-article-default')
                postUrl = 'https://www.pttweb.cc' + linkElement['href']
                driverEachPost = myFun.enterBoard(postUrl)
                soupEachPost = myFun.BeautifulSoup(driverEachPost.page_source, 'html.parser')
                
                # Obtain post meta info: ID, AUTHOR, BOARD, TIME_STAMP
                metaInfo = myFun.getPostMetaInfo(soupEachPost, postUrl)
                ID = metaInfo[0]
                if(metaInfo[1] != -1):
                    AUTHOR = metaInfo[1]
                BOARD = metaInfo[2]
                if(metaInfo[3] != -1):
                    TIME_STAMP = metaInfo[3]

                # Obtain post content: CONTENT, AUTHOR_IP
                allCont = soupEachPost.find_all('div', class_ = 'e7-main-content')
                tmp = myFun.getPostCont(allCont)
                CONTENT = tmp[0]
                AUTHOR_IP = tmp[1]

                #CONTENT = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit,'

                # Obtain comments/rating/commenters
                # comtAndRating = myFun.getComt(allCont)
                # COMMENTS = comtAndRating[0]
                # RATING = comtAndRating[1]
                # COMMENTERS = comtAndRating[2]
                # POLARITY = comtAndRating[3]

                #comtAndRating = myFun.getComt(allCont)
                COMMENTS = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit,'
                RATING = '123'
                COMMENTERS = 'JohnDoe'
                POLARITY = '123'

                # Close the driver for the post page
                driverEachPost.close()

                # Write data into data set
                eachData = [ID, TITLE, AUTHOR, BOARD, CONTENT, TIME_STAMP, AUTHOR_IP, COMMENTS, RATING, COMMENTERS, POLARITY]
                dataSet.append(eachData)

    # Close the driver for the index page            
    driverIdx.quit()

    # Output the data
    df = myFun.pd.DataFrame(dataSet)
    df.columns = ["ID", "TITLE", "AUTHOR", "BOARD", "CONTENT", "TIME_STAMP", "AUTHOR_IP", "COMMENTS", "RATING", "COMMENTERS", "POLARITY"]
    df.to_csv("output.csv")

    return 0