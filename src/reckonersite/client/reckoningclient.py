'''
Created on Aug 25, 2011
@author: danko
'''
import urllib2

from django.conf import settings
from reckonersite.domain.reckoning import Reckoning
from reckonersite.domain.reckoningservicelist import ReckoningServiceList
from reckonersite.domain.serviceresponse import ServiceResponse

def client_post_reckoning(reckoning, user_token):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/reckoning"
    
    reckoning.interval = "604800000"
    reckoning.anonymous_requested = False
    
    req = urllib2.Request(url = url,
                          data = reckoning.getPostingXMLString(user_token),
                          headers = {'Content-Type': 'text/xml'})

    response = urllib2.urlopen(req)
    content = response.read()
    servResponse = ServiceResponse(xml_string = content)
    
    return servResponse

def client_get_reckoning(id, user_token):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/reckoning/" + id + "?user_token=" + user_token
    
    response = urllib2.urlopen(url)
    content = response.read()
    reckoningList = ReckoningServiceList(xml_string = content)

    return reckoningList   
    
    
        