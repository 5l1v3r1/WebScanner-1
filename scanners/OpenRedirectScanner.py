# -*- coding: utf-8 -*-

from Scanner import Scanner
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

class Parameters:

    def __init__(self, param, value):
        self.param = param
        self.value = value

class OpenRedirectScanner(Scanner):
    className = "Open Redirect"
    results = { 'class': className, 'results': {} }

    # Overloading Method.
    def scanVulnerabilities(self):

        # For Each Target..
        for target in self.targets:
            print
            print '[OPEN REDIRECT] Scanning ' + target['action'] + ' ...'
            print

            # Set Method
            method = target['method']

            # Extract Parameters
            unmoddedParams = []

            for input in target['inputs']:
                unmoddedParams.append(input['name'])


            # Prepare Parameters in OOP if we wish to fill in the values.
            # If no "=" detected in param string, assume empty param for injection.
            # Sample: {"username" = "john", "password" = "123456"}

            # NOTE: Main Scanner does not support value in parameters. Shoudn't affect much though...

            paramsArray = [] # Array of Parameter Objects
            paramsArray = self._splitParams(unmoddedParams)

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
            print '[OPEN REDIRECT] NOTE: FIRST TWO PAYLOADS ARE GUARANTEED TO FAIL FOR TESTING PURPOSES.'
            print

            noResult = True

            for payload in payloads:
                print '[OPEN REDIRECT] Trying with payload: ' + payload + ' ...'
                KVParams = self._constructKVPair(payload, paramsArray)
                isSuccess = self._sendPayload(target['action'], KVParams, method, "", True)
                # Check Payload Succeeds or Not
                if isSuccess:
                    print '[OPEN REDIRECT] .... Success.'
                    print
                    # Generate Result List
                    noResult = False
                    self._generateResult(target['action'], KVParams, method)
                    print
                    print '[OPEN REDIRECT] Vulnerability found for ' + target['action']
                    print
                    break # Exit For Loop. Mission is Done.
                else:
                    print '[OPEN REDIRECT] .... Failed.'
                    print
            # Failed to find any...
            if noResult:
                print
                print '[OPEN REDIRECT] No result for ' + target['action']
                print

        return self.results


    def _generateResult(self, target, KVParams, method):

        parsed_uri = urlparse(target)
        domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        path = '{uri.path}'.format(uri=parsed_uri)

        if domain not in self.results['results']:
            self.results['results'][domain] = [{
                'endpoint' : path,
                'params' : KVParams,
                'method' : method
            }]
        else:
            self.results['results'][domain].append({
                'endpoint' : path,
                'params' : KVParams,
                'method' : method
            })

    def _sendPayload(self, target, KVParams, method, cookies, performDoubleCheck):
        try:
            if method == "GET":
                response = requests.get(target, params=KVParams, timeout=10)
            else: # Sending as POST
                response = requests.post(target, data=KVParams, timeout=10)

            try:
                if response.history:
                    # Redirection Detected

                    # Perform Check To Ensure Page Is Correct (Perhaps perform more robust check?)...?
                    # .... Example: Search for the text in response: We continuously monitor the status of github.com and all its related services.
                    if response.status_code == 200 and response.url == 'https://status.github.com/messages':
                        # Re-run with same payload again if performDoubleCheck is true
                        if performDoubleCheck:
                            doubleCheckSuccess = self._sendPayload(target, KVParams, method, cookies, False)
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

    def _constructKVPair(self, payload, toSendParams):
        KVPair = {}
        for item in toSendParams:
            if not getattr(item, 'value'):
                # Empty Param Value: Insert Payload
                # print 'Empty Param: ' + getattr(item, 'param')
                KVPair[getattr(item, 'param')] = payload
            else:
                KVPair[getattr(item, 'param')] = getattr(item, 'value')
        return KVPair

    def _splitParams(self, arrayNotSplit):
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
