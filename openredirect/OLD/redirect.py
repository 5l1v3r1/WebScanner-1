#!/usr/bin/python

import requests
import sys
import time
import os


def main():

    # first argument - file with subdomains
    file = sys.argv[1]

    # second argument - payload string
    payload = sys.argv[2]

    # open file with subdomains and iterates
    with open(file) as f:
        time.sleep(0)

        # loop for find the trace of all requests (303 is an open redirect) see the final destination
        for line in f:
            try:
                line2 = line.strip()
                line3 = line2
                # print line3
                response = requests.get(line3,params={'redirect': payload})
                # print response
                try:
                    if response.history:
                        # print 'Request was redirected'
                        # for resp in response.history:
                            # print '|'
                            # print resp.status_code, resp.url
                        # print 'Final destination:'
                        # print '+'
                        print response.status_code, response.url
                    else:
                        print 'Request was not redirected'
                except:
                    print 'connection error :('
            except:
                print 'quitting..'
try:
    start = time.time()
    main()
    end = time.time()
    print(end - start)
except IndexError:
    print ' Usage: python ' + sys.argv[0] \
        + ' [subdomains.file] [redirect.payload]\n'
    print ' Example python ' + sys.argv[0] \
        + " uber.list '//yahoo.com/%2F..'\n"