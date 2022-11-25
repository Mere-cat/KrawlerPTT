import functions as myFun
import requests

def crawl(board, totalPage, dataSet):
    url = 'https://www.ptt.cc/bbs/' + board + '/index.html'

    # Check if web page exists
    rsp = requests.get(url).status_code
    if(rsp != 200): return -1

    for curPage in range(totalPage):
        # Enter a new index page
        driver = myFun.enterBoard(url);
        
        # Get the elements in this page
        soup = myFun.BeautifulSoup(driver.page_source, 'html.parser')
        posts = soup.find_all('div', class_='r-ent')

        # Next page url
        partUrl = str(soup.select_one('#action-bar-container div.action-bar div.btn-group.btn-group-paging a:nth-of-type(2)')['href'])
        url = 'https://www.ptt.cc' + partUrl
                
        for post in posts:
            # for i in range(1):
            # enter each post page
            if post.find('div', class_='title').getText().strip()[0: 8] != '(本文已被刪除)':
                postUrl = 'https://www.ptt.cc' + post.find('div', class_='title').a['href'].strip()
                #postUrl = 'https://www.ptt.cc/bbs/Gossiping/M.1669359330.A.E69.html'
                driver = myFun.enterBoard(postUrl)
                soup = myFun.BeautifulSoup(driver.page_source, 'html.parser')
                allCont = soup.find('div', id = 'main-container')

                # Obtain post meta info
                metaInfo = myFun.getPostMeatInfo(soup, postUrl)
                ID = metaInfo[0]
                TITLE = metaInfo[1]
                AUTHOR = metaInfo[2]
                BOARD = metaInfo[3]
                TIME_STAMP = metaInfo[4]
                AUTHOR_IP = metaInfo[5]

                # Obtain post content
                CONTENT = myFun.getPostCont(allCont)

                # Obtain comments/rating/commenters
                comtAndRating = myFun.getComt(allCont)
                COMMENTS = comtAndRating[0]
                RATING = comtAndRating[1]
                COMMENTERS = comtAndRating[2]
                POLARITY = comtAndRating[3]

                # Write data into data set
                eachData = [ID, TITLE, AUTHOR, BOARD, CONTENT, TIME_STAMP, AUTHOR_IP, COMMENTS, RATING, COMMENTERS, POLARITY]
                dataSet.append(eachData)
                driver.quit()

    df = myFun.pd.DataFrame(dataSet)
    df.columns = ["ID", "TITLE", "AUTHOR", "BOARD", "CONTENT", "TIME_STAMP", "AUTHOR_IP", "COMMENTS", "RATING", "COMMENTERS", "POLARITY"]
    df.to_csv("output.csv")

    return 0