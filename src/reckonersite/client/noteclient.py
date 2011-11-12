'''
Created on Oct 17, 2011
@author: danko
'''
import urllib2
import datetime

from django.conf import settings
from reckonersite.domain.contentservicelist import ContentServiceList
from reckonersite.domain.reckoningservicelist import ReckoningServiceList
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

def client_get_flagged_reckonings(flagged_after=None, page=None, size=None, session_id=None):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/notes/reckoning/flag?"
    if (flagged_after):
        url += "flagged_after=" + flagged_after.isoformat() + "&"  
    if (page is not None):
        url += "page=" + str(page) + "&" 
    if (size):
        url += "size=" + str(size) + "&" 
    if (session_id):
        url += "session_id=" + session_id + "&"

    response = urllib2.urlopen(url)    
    content = response.read()
    reckoningList = ReckoningServiceList(xml_string = content)
    
    return reckoningList 

def client_get_flagged_reckoning_comments(flagged_after=None, page=None, size=None, session_id=None):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/notes/reckoning/comment/flag?"
    if (flagged_after):
        url += "flagged_after=" + flagged_after.isoformat() + "&"  
    if (page is not None):
        url += "page=" + str(page) + "&" 
    if (size):
        url += "size=" + str(size) + "&" 
    if (session_id):
        url += "session_id=" + session_id + "&"

    response = urllib2.urlopen(url)    
    content = response.read()
    reckoningList = ReckoningServiceList(xml_string = content)
    
    return reckoningList 

def client_post_content_favorite(favorite, content_id, session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/notes/content/favorite/" + content_id
    if (session_id):
        url += "?session_id=" + session_id
        
    req = urllib2.Request(url = url,
                          data = favorite.getPostingXMLString(session_id),
                          headers = {'Content-Type': 'text/xml'})

    response = urllib2.urlopen(req)
    content = response.read()
    servResponse = ServiceResponse(xml_string = content)
    
    return servResponse    

def client_post_content_flag(flag, content_id, session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/notes/content/flag/" + content_id
    if (session_id):
        url += "?session_id=" + session_id
    
    print "Content Flag: " + url
    print "Content Flag: " + flag.getPostingXMLString(session_id)
    
    req = urllib2.Request(url = url,
                          data = flag.getPostingXMLString(session_id),
                          headers = {'Content-Type': 'text/xml'})

    response = urllib2.urlopen(req)
    content = response.read()
    servResponse = ServiceResponse(xml_string = content)
    
    return servResponse 

def client_post_content_comment_favorite(favorite, comment_id, session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/notes/content/comment/favorite/" + comment_id
    if (session_id):
        url += "?session_id=" + session_id
        
    req = urllib2.Request(url = url,
                          data = favorite.getPostingXMLString(session_id),
                          headers = {'Content-Type': 'text/xml'})

    response = urllib2.urlopen(req)
    content = response.read()
    servResponse = ServiceResponse(xml_string = content)
    
    return servResponse 

def client_post_content_comment_flag(flag, comment_id, session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/notes/content/comment/flag/" + comment_id    
    if (session_id):
        url += "?session_id=" + session_id
        
    req = urllib2.Request(url = url,
                          data = flag.getPostingXMLString(session_id),
                          headers = {'Content-Type': 'text/xml'})

    response = urllib2.urlopen(req)
    content = response.read()
    servResponse = ServiceResponse(xml_string = content)
    
    return servResponse 

def client_get_flagged_contents(flagged_after=None, page=None, size=None, session_id=None):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/notes/content/flag?"
    if (flagged_after):
        url += "flagged_after=" + flagged_after.isoformat() + "&"  
    if (page is not None):
        url += "page=" + str(page) + "&" 
    if (size):
        url += "size=" + str(size) + "&" 
    if (session_id):
        url += "session_id=" + session_id + "&"

    response = urllib2.urlopen(url)    
    content = response.read()
    contentList = ContentServiceList(xml_string = content)
    
    return contentList 

def client_get_flagged_content_comments(flagged_after=None, page=None, size=None, session_id=None):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/notes/content/comment/flag?"
    if (flagged_after):
        url += "flagged_after=" + flagged_after.isoformat() + "&"  
    if (page is not None):
        url += "page=" + str(page) + "&" 
    if (size):
        url += "size=" + str(size) + "&" 
    if (session_id):
        url += "session_id=" + session_id + "&"

    response = urllib2.urlopen(url)    
    content = response.read()
    contentList = ContentServiceList(xml_string = content)
    
    return contentList 