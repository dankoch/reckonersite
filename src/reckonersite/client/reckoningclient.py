'''
Created on Aug 25, 2011
@author: danko
'''
import urllib2
import datetime

from django.conf import settings
from reckonersite.client.utilities import url_encode_list
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

def client_get_reckonings(posted_before=None, posted_after=None, closed_before=None, closed_after=None,
                          include_tags=None, exclude_tags=None,
                          sort_by=None, ascending=False, page=None, size=None,
                          session_id=None):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/reckoning" + "?"
    if (posted_before):
        url += "posted_before=" + posted_before.isoformat() + "&"    
    if (posted_after):
        url += "posted_after=" + posted_before.isoformat() + "&"  
    if (closed_before):
        url += "closed_before=" + posted_before.isoformat() + "&"  
    if (closed_after):
        url += "closed_after=" + posted_before.isoformat() + "&"  
    if (include_tags):
        url += "include_tags=" + url_encode_list(include_tags) + "&"  
    if (exclude_tags):
        url += "exclude_tags=" + url_encode_list(exclude_tags) + "&"  
    if (sort_by):
        url += "sort_by=" + sort_by + "&" 
    if (ascending):
        url += "ascending=true" + "&"
    if (page):
        url += "page=" + str(page) + "&" 
    if (size):
        url += "size=" + str(size) + "&" 
    if (session_id):
        url += "session_id=" + session_id + "&"
    
    response = urllib2.urlopen(url)    
    content = response.read()
    reckoningList = ReckoningServiceList(xml_string = content)
    
    return reckoningList   

def client_get_open_reckonings(posted_before=None, posted_after=None, closed_before=None, closed_after=None,
                          include_tags=None, exclude_tags=None,
                          sort_by=None, ascending=False, page=None, size=None,
                          session_id=None):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/reckoning/open" + "?"
    if (posted_before):
        url += "posted_before=" + posted_before.isoformat() + "&"    
    if (posted_after):
        url += "posted_after=" + posted_before.isoformat() + "&"  
    if (closed_before):
        url += "closed_before=" + posted_before.isoformat() + "&"  
    if (closed_after):
        url += "closed_after=" + posted_before.isoformat() + "&"  
    if (include_tags):
        url += "include_tags=" + url_encode_list(include_tags) + "&"  
    if (exclude_tags):
        url += "exclude_tags=" + url_encode_list(exclude_tags) + "&"  
    if (sort_by):
        url += "sort_by=" + sort_by + "&" 
    if (ascending):
        url += "ascending=true" + "&"
    if (page):
        url += "page=" + str(page) + "&" 
    if (size):
        url += "size=" + str(size) + "&" 
    if (session_id):
        url += "session_id=" + session_id + "&"
    
    response = urllib2.urlopen(url)    
    content = response.read()
    reckoningList = ReckoningServiceList(xml_string = content)
    
    return reckoningList 

def client_get_closed_reckonings(posted_before=None, posted_after=None, closed_before=None, closed_after=None,
                          include_tags=None, exclude_tags=None,
                          sort_by=None, ascending=False, page=None, size=None,
                          session_id=None):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/reckoning/closed" + "?"
    if (posted_before):
        url += "posted_before=" + posted_before.isoformat() + "&"    
    if (posted_after):
        url += "posted_after=" + posted_before.isoformat() + "&"  
    if (closed_before):
        url += "closed_before=" + posted_before.isoformat() + "&"  
    if (closed_after):
        url += "closed_after=" + posted_before.isoformat() + "&"  
    if (include_tags):
        url += "include_tags=" + url_encode_list(include_tags) + "&"  
    if (exclude_tags):
        url += "exclude_tags=" + url_encode_list(exclude_tags) + "&"  
    if (sort_by):
        url += "sort_by=" + sort_by + "&" 
    if (ascending):
        url += "ascending=true" + "&"
    if (page):
        url += "page=" + str(page) + "&" 
    if (size):
        url += "size=" + str(size) + "&" 
    if (session_id):
        url += "session_id=" + session_id + "&"
    
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

def client_get_open_highlighted_reckonings(page, size, session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/reckoning/highlighted/open?"
    if (page):
        url += "page=" + str(page) + "&" 
    if (size):
        url += "size=" + str(size) + "&" 
    if (session_id):
        url += "session_id=" + session_id + "&"
           
    response = urllib2.urlopen(url)    
    content = response.read()
    reckoningList = ReckoningServiceList(xml_string = content)
    
    return reckoningList       