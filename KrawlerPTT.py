"""
This is the main script of the KrawlerPTT.
-----------------------------------------------------------------

KrawlerPTT is a simple crawler for PTT, the commonly used BBS in
Taiwan. Users can specify the board and the number of posts they
want to crawl within KrawlerPTT. If they don't, KrawlerPTT will 
crawl 10 posts in Gossiping board by default.

This program is mainly checking for the command user inputed, if
the command is valid, it will do the crawling and print out the 
success message.
"""

import crawler
import getopt, sys
import default_var as DFLT

dataSet = [
    # we have 11 columns in each row
    # ["ID", "TITLE", "AUTHOR", "BOARD", "CONTENT", "TIME_STAMP", "AUTHOR_IP", "COMMENTS", "RATING", "COMMENTERS", "POLARITY", "IMG_SRC"]
]

def main():
    # Set the default values
    board = 'Gossiping'
    totalPost = DFLT.DEFAULT_POSTS

    # Read the command line arguments
    argv = sys.argv[1:]

    try:
        # Command line argument:
        # -b: the board user want to crawl
        # -n: the number of posts user want to crawl
        opts, args = getopt.getopt(argv, "b:n:")

    except:
        # If user input an invalid command line argument, print error message
        print("[Error] invalid argument")

    # Read the argument
    for opt,arg in opts:
        # Read the -b argument
        if opt in ['-b']:
            board = arg
        # Read the -n argument
        elif opt in ['-n']:
            totalPost = int(arg) # cast the input to int type
            # Check if the number of posts user input is positive
            # If not, print the error message and return
            if(totalPost <= 0):
                print('[ERROR] number of posts should be positive.')
                return 1

    # Check if the board user input exists
    # The function crawl() will execute the crawling work.
    # If the board user input exists, crawl() will crawl the user-specific number of posts in the specific board
    # and return 0, printing out the success message
    # If the board doesn't exist, crawl() returns -1
    valid = crawler.crawl(board, totalPost, dataSet)
    if(valid == 0):
        print('KrawlerPTT executed successfully. The result was output as "output.csv".')
    else:
        print('[ERROR] The board does not exist.')

    # End the program if successfully executed
    return 0

if __name__ == '__main__':
    main()
