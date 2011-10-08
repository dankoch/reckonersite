'''
Created on Aug 25, 2011
@author: danko
'''
import urllib2

from django.conf import settings
from reckonersite.domain.serviceresponse import ServiceResponse
from reckonersite.domain.vote import Vote
from reckonersite.domain.voteservicelist import VoteServiceList

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


def client_get_user_reckoning_vote(reckoning_id, user_id, session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/vote/user/" + user_id + \
        "/reckoning/" + reckoning_id + "?"
    if (session_id):
        url += "session_id=" + session_id + "&"
    
    response = urllib2.urlopen(url)
    content = response.read()
    voteList = VoteServiceList(xml_string = content)

    return voteList   
