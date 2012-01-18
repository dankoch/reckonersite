'''
Created on Aug 25, 2011
@author: danko
'''
import urllib2

from django.conf import settings
from reckonersite.domain.reckoningservicelist import ReckoningServiceList
from reckonersite.domain.serviceresponse import ServiceResponse
from reckonersite.domain.voteservicelist import VoteServiceList

def client_post_reckoning_vote(vote, reckoning_id, answer_index, session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/vote/reckoning/" \
                                 + reckoning_id + "/answer/" + answer_index

    req = urllib2.Request(url = url,
                          data = vote.getPostingXMLString(session_id),
                          headers = {'Content-Type': 'text/xml'})

    response = urllib2.urlopen(req)
    content = response.read()
    servResponse = ServiceResponse(xml_string = content)
    
    return servResponse


def client_update_reckoning_vote(vote, session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/vote/update"

    req = urllib2.Request(url = url,
                          data = vote.getPostingXMLString(session_id),
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


def client_get_user_reckoning_votes(user_id, page, size, session_id):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/vote/user/" + user_id + "?"
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

def client_get_reckoning_answer_votes(reckoning_id, answer_index, page=None, size=None, session_id=None):
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/vote/reckoning/" \
                                 + reckoning_id + "/answer/" + answer_index + "?"
    if (page is not None):
        url += "page=" + str(page) + "&" 
    if (size):
        url += "size=" + str(size) + "&" 
    if (session_id):
        url += "session_id=" + session_id + "&"
    
    response = urllib2.urlopen(url)
    content = response.read()
    voteList = VoteServiceList(xml_string = content)

    return voteList  