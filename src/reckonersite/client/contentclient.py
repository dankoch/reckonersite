'''
Created on Nov 10, 2011
@author: danko
'''
import urllib
import urllib2

from django.conf import settings
from reckonersite.client.utilities import url_encode_list
from reckonersite.domain.contentservicelist import ContentServiceList
from reckonersite.domain.dataservicelist import DataServiceList
from reckonersite.domain.serviceresponse import ServiceResponse

def client_post_content(content, session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/content"
    
    content.anonymous_requested = False
    
    req = urllib2.Request(url = url,
                          data = content.getPostingXMLString(session_id),
                          headers = {'Content-Type': 'text/xml'})

    response = urllib2.urlopen(req)
    content = response.read()
    servResponse = ServiceResponse(xml_string = content)
    
    return servResponse

def client_update_content(content, session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/content/update"
    
    req = urllib2.Request(url = url,
                          data =content.getPostingXMLString(session_id),
                          headers = {'Content-Type': 'text/xml'})

    response = urllib2.urlopen(req)
    content = response.read()
    servResponse = ServiceResponse(xml_string = content)
       
    return servResponse


def client_get_content(id, session_id, include_unaccepted=False, page_visit=False):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/content/id/" + id + "?"
    if (session_id):
        url += "session_id=" + session_id + "&"
    if (include_unaccepted):
        url += "include_unaccepted=true" + "&"
    if (page_visit):
        url += "page_visit=true" + "&"

    response = urllib2.urlopen(url)    
    content = response.read()
    contentList = ContentServiceList(xml_string = content)
    
    return contentList   


def client_get_contents(content_type=None, posted_before=None, posted_after=None,
                          include_tags=None, submitted_by=None,
                          sort_by=None, ascending=False, page=None, size=None, randomize=None, count_only=None,
                          session_id=None):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/reckoning" + "?"
    if (content_type):
        url += "content_type=" + content_type + "&"  
    if (posted_before):
        url += "posted_before=" + posted_before.isoformat() + "&"    
    if (posted_after):
        url += "posted_after=" + posted_before.isoformat() + "&"  
    if (include_tags):
        if (isinstance(include_tags, list) or isinstance(include_tags, tuple)):
            url += "include_tags=" + url_encode_list(include_tags) + "&" 
        else:
            url += "include_tags=" + urllib.quote_plus(include_tags) + "&"    
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
    if (count_only):
        url += "count_only=true&"        
    if (session_id):
        url += "session_id=" + session_id + "&"
    
    response = urllib2.urlopen(url)    
    content = response.read()
    contentList = ContentServiceList(xml_string = content)
    
    return contentList  

def client_get_content_types(session_id):
    '''
    Receives the list of permissions the Reckoner currently uses.
    '''
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/list/user/contenttypes?" + session_id
    
    response = urllib2.urlopen(url)
    content = response.read()
    servResponse = DataServiceList(xml_string = content)

    return servResponse    

def client_reject_content(content_id, session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/content/reject/" + content_id
    if (session_id):
        url += "?session_id=" + session_id
    
    response = urllib2.urlopen(url)
    content = response.read()
    servResponse = ServiceResponse(xml_string = content)
    
    return servResponse    