#!/usr/bin/env python

import shodan
import argparse
import os
import os.path

#--------------------
# Global Variables:
#--------------------
SHODAN_API_KEY = "None"
directory = "None"
params = "None"
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
    parser.add_argument("-s", "--search", dest="Search", required="true" ,help="Seach parameters", metavar='')
    parser.add_argument("-d", "--directory", dest="Directory",metavar='', help="Choose Directory to save data")
    parser.add_argument("-p", "--pages", dest="Pages", metavar='', default=1, help="Number of page results to be listed")
    args = parser.parse_args()

    global params
    params = str(args.Search)
    global directory
    directory = str(args.Directory)
    global SHODAN_API_KEY
    SHODAN_API_KEY = str(args.API_KEY)
    global api
    api = shodan.Shodan(SHODAN_API_KEY)
    global pages
    pages = int(args.Pages)
    if directory == "None":
        print("[+] directory is null, storing to current working directory.")


def createFiles():
    global ifile
    global dfile
    if directory != "None":
        if (os.path.exists(directory + '/ips.txt') or os.path.exists(directory + '/data.txt')):
            print("[+] Files already exists, appending data to files. ")
            ifile = open(directory + '/ips.txt', 'a+')
            dfile = open(directory + '/data.txt', 'a+')
        else:
            ifile = open(directory + '/ips.txt', 'w')
            dfile = open(directory + '/data.txt', 'w')
        print("Saving data to: " + directory)
    else:
        if (os.path.isfile('ips.txt') or os.path.isfile('data.txt')):
            print('[+] Files already exists, appending data to files. ')
            ifile = open('ips.txt', "a+")
            dfile = open('data.txt', 'a+')
        else:
            ifile = open('ips.txt', 'w')
            dfile = open('data.txt', 'w')

#==================
# MAIN
#==================

logo()
argParse()
results = api.search(params)


# Check if the total number of results is smaller than the page results to avoid exceptions
if (pages > 1 and 100*pages > int(results['total'])):
    print("[+] Page request is too large as there are only " + str(results['total']) + " total results. Lower your page request!")
    print("[+] Exiting Program.")
    exit(1)

# Create Files to store data & add data:
createFiles()
print("[+] Searching for: " + params)
print("[+] Results Found: %s" % results['total'])
ifile.write('Total Results: %s \n' % results['total'])
for i in range (0, pages):
    try:
        results = api.search(params, page=i)
        for result in results['matches']:
            data = ('%s' % result['data']).encode('utf-8').strip()
            dfile.write(str(data)+"\n")
            ifile.write('%s \n' % result['ip_str'])
    except shodan.APIError as e:
        print('!!! [+] Error: %s' % e)
ifile.close()
dfile.close()
print("[+] Done.")


