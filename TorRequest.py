#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
TorRequest class opens a Tor circuit and requests a
given website with anonymized Tor IP address.
'''

__author__ = 'Chris [https://github.com/RootDev4/]'
__copyright__ = 'Copyright 2020'
__license__ = 'MIT'
__version__ = "1.0.1"

import sys, re, socket
from os import path
from subprocess import Popen, PIPE

try:
    import requests
except:
    print('[-] Please install "requests" module.')
    sys.exit(1)

try:
    import socks
except:
    print('[-] Please install "pysocks" module.')
    sys.exit(1)

try:
    from subprocess import DEVNULL
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')

class TorRequest:

    # Constructor.
    # Takes path to Tor executable as argument.
    # Optional: List of HTTP headers (e.g. User Agent)
    def __init__(self, torExecPath, headers = {}):
        self.__session = requests.Session()
        self.__headers = headers
        self.__session.proxies = {}
        self.__session.proxies['http'] = 'socks5h://localhost:9050'
        self.__session.proxies['https'] = 'socks5h://localhost:9050'
        self.__isConnected = False
        self.__torIpAddress = None
        self.__runTor(torExecPath)

    # Get website.
    # Takes URL of website as argument.
    # Optional: send True as last argument, to get response object.
    def get(self, url, resObj = False):
        if self.__isConnected:
            req = self.__session.get(url, headers=self.__headers)
            if resObj:
                return req
            return req.text.strip()
        else:
            print('[-] Tor is not running.')
            return None

    # Send POST request to website and return response text.
    # Takes URL of website and POST data as arguments.
    # Optional: send True as last argument, to get response object.
    def post(self, url, payload, resObj = False):
        if self.__isConnected:
            req = self.__session.post(url, data=payload, headers=self.__headers)
            if resObj:
                return req
            return req.text.strip()
        else:
            print('[-] Tor is not running.')
            return None

    # Get connection status. Return true or false.
    def status(self):
        return self.__isConnected

    # Get IP address of Tor circuit.
    def ipAddr(self):
        return self.__torIpAddress

    # Get requests session object.
    def session(self):
        return self.__session

    # Run Tor executable and build connection circuit.
    # Private method.
    def __runTor(self, torExecPath):
        try:
            Popen(path.realpath(torExecPath), shell=False, stdout=PIPE, stderr=DEVNULL)
            self.__checkTor()
        except Exception as error:
            print('[-] %s' % error)
            sys.exit(1)

    # Check if Tor is connected successfully by requesting official Tor project website.
    # Private method.
    def __checkTor(self):
        req = self.__session.get(r'https://check.torproject.org/', headers=self.__headers)
        if 'Congratulations' in req.text:
            self.__isConnected = True
            self.__torIpAddress = re.search(r'<strong>(.*?)<\/strong>', req.text).group(1)
        else:
            raise Exception('Tor is not running.')