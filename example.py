#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
Example script for TorRequest usage
'''

from TorRequest import TorRequest

if __name__ == '__main__':
    torReq = TorRequest('<full_path_to>/tor.exe')
    if (torReq.status()):
        print('Tor is running with IP address %s' % torReq.ipAddr())
        print(torReq.get('https://icanhazip.com/')) # HTML content
        print(torReq.get('https://icanhazip.com/', True).status_code) # HTTP status code