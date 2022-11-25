import crawler
import getopt, sys

dataSet = [
    # we have 11 columns in each row
    # ["ID", "TITLE", "AUTHOR", "BOARD", "CONTENT", "TIME_STAMP", "AUTHOR_IP", "COMMENTS", "RATING", "COMMENTERS", "POLARITY"]
]

def main():
    board = 'Gossiping'
    totalPage = 1
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "b:p:")

    except:
        print("Error")

    for opt,arg in opts:
        if opt in ['-b']:
            board = arg
        elif opt in ['-p']:
            totalPage = int(arg)
            if(totalPage <= 0):
                print('[ERROR] number of page should be positive.')
                return 1

    valid = crawler.crawl(board, totalPage, dataSet)
    if(valid == 0):
        print('KrawlerPTT executed successfully. The result was output as "output.csv".')
    else:
        print('[ERROR] The board does not exist.')

    return 0

if __name__ == '__main__':
    main()
