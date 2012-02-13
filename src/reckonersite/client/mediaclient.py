'''
Created on Oct 10, 2011
@author: danko
'''
import urllib2

from django.conf import settings
from reckonersite.domain.contentservicelist import ContentServiceList
from reckonersite.domain.reckoningservicelist import ReckoningServiceList
from reckonersite.domain.serviceresponse import ServiceResponse

def client_post_reckoning_media(media, reckoning_id, session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/media/reckoning/" + reckoning_id + "?"
    
    req = urllib2.Request(url = url,
                          data = media.getPostingXMLString(session_id),
                          headers = {'Content-Type': 'text/xml'})

    response = urllib2.urlopen(req)
    content = response.read()
    servResponse = ServiceResponse(xml_string = content)
    
    return servResponse
        
def client_get_reckoning_media(media_id, session_id=None):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/media/reckoning/" + media_id + "?"
    if (session_id):
        url += "session_id=" + session_id + "&"
    
    response = urllib2.urlopen(url)
    content = response.read()
    reckoningList = ReckoningServiceList(xml_string = content)

    return reckoningList  

def client_delete_reckoning_media(media_id, session_id=None):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/media/reckoning/delete/" + media_id + "?"
    if (session_id):
        url += "session_id=" + session_id + "&"
        
    response = urllib2.urlopen(url)    
    content = response.read()
    servResponse = ServiceResponse(xml_string = content)
    
    return servResponse 

def client_post_content_media(media, content_id, session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/media/content/" + content_id + "?"
    
    req = urllib2.Request(url = url,
                          data = media.getPostingXMLString(session_id),
                          headers = {'Content-Type': 'text/xml'})

    response = urllib2.urlopen(req)
    content = response.read()
    servResponse = ServiceResponse(xml_string = content)
    
    return servResponse
        
def client_get_content_media(media_id, session_id=None):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/media/content/" + media_id + "?"
    if (session_id):
        url += "session_id=" + session_id + "&"
    
    response = urllib2.urlopen(url)
    content = response.read()
    reckoningList = ContentServiceList(xml_string = content)

    return reckoningList  

def client_delete_content_media(media_id, session_id=None):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/media/content/delete/" + media_id + "?"
    if (session_id):
        url += "session_id=" + session_id + "&"
        
    response = urllib2.urlopen(url)    
    content = response.read()
    servResponse = ServiceResponse(xml_string = content)
    
    return servResponse 