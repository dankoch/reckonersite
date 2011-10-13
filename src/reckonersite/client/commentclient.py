'''
Created on Oct 10, 2011
@author: danko
'''
import urllib2

from django.conf import settings
from reckonersite.domain.serviceresponse import ServiceResponse

def client_post_reckoning_comment(comment, reckoning_id, session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/comments/reckoning/" + reckoning_id
    
    req = urllib2.Request(url = url,
                          data = comment.getPostingXMLString(session_id),
                          headers = {'Content-Type': 'text/xml'})

    response = urllib2.urlopen(req)
    content = response.read()
    servResponse = ServiceResponse(xml_string = content)
    
    return servResponse
        