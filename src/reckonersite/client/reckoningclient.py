'''
Created on Aug 25, 2011
@author: danko
'''
import urllib
import urllib2

from django.conf import settings
from reckonersite.client.utilities import url_encode_list
from reckonersite.domain.reckoningservicelist import ReckoningServiceList
from reckonersite.domain.serviceresponse import ServiceResponse

def client_post_reckoning(reckoning, session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/reckoning"
    
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
                          include_tags=None, exclude_tags=None, highlighted=None,
                          sort_by=None, ascending=False, page=None, size=None, randomize=None,
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
        if (isinstance(include_tags, list) or isinstance(include_tags, tuple)):
            url += "include_tags=" + url_encode_list(include_tags) + "&" 
        else:
            url += "include_tags=" + urllib.quote_plus(include_tags) + "&"  
    if (exclude_tags):
        if (isinstance(exclude_tags, list) or isinstance(exclude_tags, tuple)):
            url += "exclude_tags=" + url_encode_list(exclude_tags) + "&" 
        else:
            url += "exclude_tags=" + urllib.quote_plus(exclude_tags) + "&"   
    if (highlighted is False):
        url += "highlighted=false&"
    if (highlighted is True):
        url += "highlighted=true&"
    if (sort_by):
        url += "sort_by=" + sort_by + "&" 
    if (ascending):
        url += "ascending=true&"
    if (page is not None):
        url += "page=" + str(page) + "&" 
    if (size):
        url += "size=" + str(size) + "&" 
    if (randomize):
        url += "randomize=true&"
    if (session_id):
        url += "session_id=" + session_id + "&"
    
    response = urllib2.urlopen(url)    
    content = response.read()
    reckoningList = ReckoningServiceList(xml_string = content)
    
    return reckoningList   

def client_get_open_reckonings(posted_before=None, posted_after=None, closed_before=None, closed_after=None,
                          include_tags=None, exclude_tags=None, highlighted=None,
                          sort_by=None, ascending=False, page=None, size=None, randomize=None,
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
        if (isinstance(include_tags, list) or isinstance(include_tags, tuple)):
            url += "include_tags=" + url_encode_list(include_tags) + "&" 
        else:
            url += "include_tags=" + urllib.quote_plus(include_tags) + "&"  
    if (exclude_tags):
        if (isinstance(exclude_tags, list) or isinstance(exclude_tags, tuple)):
            url += "exclude_tags=" + url_encode_list(exclude_tags) + "&" 
        else:
            url += "exclude_tags=" + urllib.quote_plus(exclude_tags) + "&"
    if (highlighted is False):
        url += "highlighted=false&"
    if (highlighted is True):
        url += "highlighted=true&"
    if (sort_by):
        url += "sort_by=" + sort_by + "&" 
    if (ascending):
        url += "ascending=true" + "&"
    if (page is not None):
        url += "page=" + str(page) + "&" 
    if (size):
        url += "size=" + str(size) + "&" 
    if (randomize):
        url += "randomize=true&"
    if (session_id):
        url += "session_id=" + session_id + "&"
    
    response = urllib2.urlopen(url)    
    content = response.read()
    reckoningList = ReckoningServiceList(xml_string = content)
    
    return reckoningList 

def client_get_closed_reckonings(posted_before=None, posted_after=None, closed_before=None, closed_after=None,
                          include_tags=None, exclude_tags=None, highlighted=None,
                          sort_by=None, ascending=False, page=None, size=None, randomize=None,
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
        if (isinstance(include_tags, list) or isinstance(include_tags, tuple)):
            url += "include_tags=" + url_encode_list(include_tags) + "&" 
        else:
            url += "include_tags=" + urllib.quote_plus(include_tags) + "&"  
    if (exclude_tags):
        if (isinstance(exclude_tags, list) or isinstance(exclude_tags, tuple)):
            url += "exclude_tags=" + url_encode_list(exclude_tags) + "&" 
        else:
            url += "exclude_tags=" + urllib.quote_plus(exclude_tags) + "&"
    if (highlighted is False):
        url += "highlighted=false&"
    if (highlighted is True):
        url += "highlighted=true&"
    if (sort_by):
        url += "sort_by=" + sort_by + "&" 
    if (ascending):
        url += "ascending=true" + "&"
    if (page is not None):
        url += "page=" + str(page) + "&" 
    if (size):
        url += "size=" + str(size) + "&" 
    if (randomize):
        url += "randomize=true&"
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
   
def client_get_related_open_reckonings(reckoning_id, size, session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/reckoning/related/" + reckoning_id + "/open?"
    if (size is not None):
        url += "size=" + str(size) + "&"  
    if (session_id):
        url += "session_id=" + session_id + "&"
    
    response = urllib2.urlopen(url)
    content = response.read()
    reckoningList = ReckoningServiceList(xml_string = content)

    return reckoningList     

def client_get_related_closed_reckonings(reckoning_id, size, session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/reckoning/related/" + reckoning_id + "/closed?"
    if (size is not None):
        url += "size=" + str(size) + "&"
    if (session_id):
        url += "session_id=" + session_id + "&"
    
    response = urllib2.urlopen(url)
    content = response.read()
    reckoningList = ReckoningServiceList(xml_string = content)

    return reckoningList     

def client_get_user_reckonings(user_id, page=None, size=None, session_id=None):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/reckoning/user/" + user_id + "?"
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

def client_get_favorited_reckonings(user_id, page=None, size=None, session_id=None):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/notes/reckoning/favorite/user/" + user_id + "?"
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