'''
Created on Aug 25, 2011
@author: danko
'''
import urllib2

from django.conf import settings
from reckonersite.domain.serviceresponse import ServiceResponse

def client_post_reckoning(reckoning, user_token):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/reckoning"
    
    req = urllib2.Request(url = url,
                          data = reckoning.getPostingXMLString(user_token),
                          headers = {'Content-Type': 'text/xml'})

    response = urllib2.urlopen(req)
    content = response.read()
    servResponse = ServiceResponse()
    servResponse.buildFromXMLString(content)
    
    return servResponse
        