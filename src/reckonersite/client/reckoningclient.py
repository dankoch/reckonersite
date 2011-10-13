'''
Created on Aug 25, 2011
@author: danko
'''
import urllib2

from django.conf import settings
from reckonersite.domain.reckoning import Reckoning
from reckonersite.domain.reckoningservicelist import ReckoningServiceList
from reckonersite.domain.serviceresponse import ServiceResponse

def client_post_reckoning(reckoning, session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/reckoning"
    
    reckoning.anonymous_requested = False
    
    req = urllib2.Request(url = url,
                          data = reckoning.getPostingXMLString(session_id),
                          headers = {'Content-Type': 'text/xml'})

    response = urllib2.urlopen(req)
    content = response.read()
    servResponse = ServiceResponse(xml_string = content)
    
    return servResponse

def client_update_reckoning(reckoning, session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/reckoning/update"
    
    req = urllib2.Request(url = url,
                          data = reckoning.getPostingXMLString(session_id),
                          headers = {'Content-Type': 'text/xml'})
    
    print "Update Reckoning: " + reckoning.getPostingXMLString(session_id)

    response = urllib2.urlopen(req)
    content = response.read()
    servResponse = ServiceResponse(xml_string = content)
       
    return servResponse


def client_get_reckoning(id, session_id, include_unaccepted=False, page_visit=False):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/reckoning/id/" + id + "?"
    if (session_id):
        url += "session_id=" + session_id + "&"
    if (include_unaccepted):
        url += "include_unaccepted=true" + "&"
    if (page_visit):
        url += "page_visit=true" + "&"
        
    response = urllib2.urlopen(url)    
    content = response.read()
    reckoningList = ReckoningServiceList(xml_string = content)
    
    return reckoningList   

def client_get_reckoning_approval_queue(session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/reckoning/approvalqueue"
    if (session_id):
        url += "?session_id=" + session_id
    
    response = urllib2.urlopen(url)    
    content = response.read()
    reckoningList = ReckoningServiceList(xml_string = content)

    return reckoningList  

def client_approve_reckoning(reckoning_id, session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/reckoning/approve/" + reckoning_id
    if (session_id):
        url += "?session_id=" + session_id
    
    response = urllib2.urlopen(url)
    content = response.read()
    servResponse = ServiceResponse(xml_string = content)
    
    return servResponse 

def client_reject_reckoning(reckoning_id, session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/reckoning/reject/" + reckoning_id
    if (session_id):
        url += "?session_id=" + session_id
    
    response = urllib2.urlopen(url)
    content = response.read()
    servResponse = ServiceResponse(xml_string = content)
    
    return servResponse      
    
def client_get_random_open_reckoning(session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/reckoning/random/open"
    if (session_id):
        url += "?session_id=" + session_id
    
    response = urllib2.urlopen(url)
    content = response.read()
    reckoningList = ReckoningServiceList(xml_string = content)

    return reckoningList  

def client_get_random_closed_reckoning(session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/reckoning/random/closed"
    if (session_id):
        url += "?session_id=" + session_id
    
    response = urllib2.urlopen(url)
    content = response.read()
    reckoningList = ReckoningServiceList(xml_string = content)

    return reckoningList  
        