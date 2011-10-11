'''
Created on Oct 10, 2011
@author: danko
'''
import urllib2

from django.conf import settings
from reckonersite.domain.serviceresponse import ServiceResponse

def client_post_reckoning_comment(comment, reckoning_id, session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/comments/reckoning/" + reckoning_id
    
    print "Post Comment 0: " + comment.getPostingXMLString(session_id)
    
    req = urllib2.Request(url = url,
                          data = comment.getPostingXMLString(session_id),
                          headers = {'Content-Type': 'text/xml'})

    print "Post Comment: " + url

    response = urllib2.urlopen(req)
    content = response.read()
    print "Post Comment 2: " + content
    servResponse = ServiceResponse(xml_string = content)
    
    return servResponse
        