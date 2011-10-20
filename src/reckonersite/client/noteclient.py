'''
Created on Oct 17, 2011
@author: danko
'''
import urllib2
import datetime

from django.conf import settings
from reckonersite.domain.serviceresponse import ServiceResponse
        
def client_post_reckoning_favorite(favorite, reckoning_id, session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/notes/reckoning/favorite/" + reckoning_id
    if (session_id):
        url += "?session_id=" + session_id
        
    req = urllib2.Request(url = url,
                          data = favorite.getPostingXMLString(session_id),
                          headers = {'Content-Type': 'text/xml'})

    response = urllib2.urlopen(req)
    content = response.read()
    servResponse = ServiceResponse(xml_string = content)
    
    return servResponse    

def client_post_reckoning_flag(flag, reckoning_id, session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/notes/reckoning/flag/" + reckoning_id
    if (session_id):
        url += "?session_id=" + session_id
        
    req = urllib2.Request(url = url,
                          data = flag.getPostingXMLString(session_id),
                          headers = {'Content-Type': 'text/xml'})

    response = urllib2.urlopen(req)
    content = response.read()
    servResponse = ServiceResponse(xml_string = content)
    
    return servResponse 

def client_post_reckoning_comment_favorite(favorite, comment_id, session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/notes/reckoning/comment/favorite/" + comment_id
    if (session_id):
        url += "?session_id=" + session_id
        
    req = urllib2.Request(url = url,
                          data = favorite.getPostingXMLString(session_id),
                          headers = {'Content-Type': 'text/xml'})

    response = urllib2.urlopen(req)
    content = response.read()
    servResponse = ServiceResponse(xml_string = content)
    
    return servResponse 

def client_post_reckoning_comment_flag(flag, comment_id, session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/notes/reckoning/comment/flag/" + comment_id    
    if (session_id):
        url += "?session_id=" + session_id
        
    req = urllib2.Request(url = url,
                          data = flag.getPostingXMLString(session_id),
                          headers = {'Content-Type': 'text/xml'})

    response = urllib2.urlopen(req)
    content = response.read()
    servResponse = ServiceResponse(xml_string = content)
    
    return servResponse 