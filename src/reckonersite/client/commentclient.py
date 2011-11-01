'''
Created on Oct 10, 2011
@author: danko
'''
import urllib2

from django.conf import settings
from reckonersite.domain.reckoningservicelist import ReckoningServiceList
from reckonersite.domain.serviceresponse import ServiceResponse

def client_post_reckoning_comment(comment, reckoning_id, session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/comments/reckoning/" + reckoning_id + "?"
    
    req = urllib2.Request(url = url,
                          data = comment.getPostingXMLString(session_id),
                          headers = {'Content-Type': 'text/xml'})

    response = urllib2.urlopen(req)
    content = response.read()
    servResponse = ServiceResponse(xml_string = content)
    
    return servResponse

def client_update_reckoning_comment(comment, session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/comments/reckoning/update?"
    
    req = urllib2.Request(url = url,
                          data = comment.getPostingXMLString(session_id),
                          headers = {'Content-Type': 'text/xml'})

    response = urllib2.urlopen(req)
    content = response.read()
    servResponse = ServiceResponse(xml_string = content)
    
    return servResponse
        
def client_get_user_comments(user_id, page=None, size=None, session_id=None):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/comments/reckoning/user/" + user_id + "?"
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

def client_get_favorited_comments(user_id, page=None, size=None, session_id=None):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/notes/reckoning/comment/favorite/user/" + user_id + "?"
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

def client_delete_reckoning_comment(comment_id, session_id=None):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/comments/reckoning/id/" + comment_id + "/delete?"
    if (session_id):
        url += "session_id=" + session_id + "&"
        
    response = urllib2.urlopen(url)    
    content = response.read()
    servResponse = ServiceResponse(xml_string = content)
    
    return servResponse 