'''
Created on Aug 25, 2011
@author: danko
'''

import urllib

def url_encode_list(list):
    encodedList = None
    
    if (list):
        for item in list:
            encodedList = "".join((encodedList, urllib.quote_plus(item.strip())))
    
    return encodedList
        