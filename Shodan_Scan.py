#!/usr/bin/env python

import shodan
import argparse
import os
import os.path
import time
import datetime

#--------------------
# Global Variables:
#--------------------
SHODAN_API_KEY = "None"
directory = "None"
params = "None"
limit = "None"
api = "None"
ifile = 'None'
dfile = 'None'
pages = 1

class bcolors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[31m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    BGRED = '\033[41m'
    WHITE = '\033[37m'

def logo():
    # Check if OS is Linux or Windows.
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")

    print(bcolors.RED + bcolors.BOLD)
    print("""
         ___    _____    ____  _               _             
        |_ _|__|_   _|  / ___|| |__   ___   __| | __ _ _ __  
         | |/ _ \| |____\___ \| '_ \ / _ \ / _` |/ _` | '_ \ 
         | | (_) | |_____|__) | | | | (_) | (_| | (_| | | | |
        |___\___/|_|    |____/|_| |_|\___/ \__,_|\__,_|_| |_|""")
    print(bcolors.WHITE + bcolors.BOLD +  "         By: Joshua Faust" + bcolors.ENDC)
    print(bcolors.ENDC)

def argParse():
    # Possible Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--api", dest="API_KEY", required="true", help="Shodan API Key", metavar='')
    parser.add_argument("-d", "--directory", dest="Directory",metavar='', help="Choose Directory to save data")
    parser.add_argument("-p", "--pages", dest="Pages", metavar='', default=1, help="Number of page results to be listed")
    parser.add_argument("-l", "--limit", dest="limit", metavar="", default=100, help="Number of records to save")
    args = parser.parse_args()

    global limit
    limit = int(args.limit)
    global directory
    directory = str(args.Directory)
    global SHODAN_API_KEY
    SHODAN_API_KEY = str(args.API_KEY)
    global api
    api = shodan.Shodan(SHODAN_API_KEY)
    global pages
    pages = int(args.Pages)


def createFiles():
    global ifile
    global dfile
    if directory != "None":
        if (os.path.exists(directory + '/searches.txt')):
            print("[+] Files already exists, appending data to files. ")
            ifile = open(directory + '/searches.txt', 'a+')
        else:
            ifile = open(directory + '/searches.txt', 'w')
        print("Saving data to: " + directory)
    else:
        if (os.path.isfile('searches.txt')):
            print('[+] Files already exists, appending data to files. ')
            ifile = open('searches.txt', "a+")
        else:
            ifile = open('searches.txt', 'w')



def errorChecking(results):
    # Check if the total number of results is smaller than the page/limit results to avoid exceptions
    if (pages > 1 and 100 * pages > int(results['total']) or limit > int(results['total'])):
        print("[+] Page request is too large as there are only " + str(
            results['total']) + " total results. Lower your page request!")
        print("[+] Exiting Program.")
        exit(1)

    elif (pages > 1 and limit > 100):
        print("You cannot specify both Pages and Limit, choose one.")
        exit(1)

#==================
# MAIN
#==================
if __name__ == "__main__":
    logo()
    argParse()
    #errorChecking(results)

    searches = ['linux upnp avtech product:"Avtech AVN801 network camera"',
                'SQ-WEBCAM product:"dvr1614n web-cam httpd"',
                'netcam product:"TRENDnet TV-IP100 or TV-IP110 webcam display httpd"',
                'port:554 has_screenshot:true', 'Heatmiser', 'product:samsung port:8001',
                'product:samsung version:"UN50H6400"', 'product:samsung version:"UN50H5800"',
                'webOS + tv/version']

    # Create Files to store data & add data:
    createFiles()
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    ifile.write(st +"\n")
    for i in range (0, len(searches)):
        results = api.search(searches[i])
        print(str(i) + ": " + searches[i] + ": " + str(results['total']))
        ifile.write(searches[i] + ": " + str(results['total']) + "\n")


ifile.close()
print("[+] Done.")


