'''
Created on Aug 25, 2011
@author: danko
'''
import urllib2

from django.conf import settings
from reckonersite.domain.authsession import AuthSession
from reckonersite.domain.dataservicelist import DataServiceList
from reckonersite.domain.oauthaccesstoken import OAuthAccessToken
from reckonersite.domain.reckoneruser import ReckonerUser
from reckonersite.domain.userserviceresponse import UserServiceResponse

def client_authenticate_user(oAuth_receipt):
    '''
    Receives the authentication information received from the OAuth provider 
    (in oauthaccesstoken form).  
    
    Checks and registers this information with the
    Reckoner Content Services and returns a UserServiceResponse
    object with the necessary information.
    '''
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/user/authentication/oauth"
    
    req = urllib2.Request(url = url,
                          data = oAuth_receipt.getXMLString(),
                          headers = {'Content-Type': 'text/xml'})

    response = urllib2.urlopen(req)
    content = response.read()
    servResponse = UserServiceResponse(xml_string = content)
        
    return servResponse

def client_logout_user(session_id):
    '''
    Receives the ID for the current session (as originally retrieved from
    the initial login - via OAuth or otherwise).  
    
    Forwards this information to the Reckoner Content Services, which deletes the associated
    session and logs the user out.
    '''
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/user/logout"
    if (session_id):
        url += "?session_id=" + session_id
    
    response = urllib2.urlopen(url)
    content = response.read()
    servResponse = UserServiceResponse(xml_string = content)

    return servResponse 

def client_get_user_summaries(active=None, sort_by=None, ascending=None, 
                              page=None, size=None, session_id=None):
    '''
    Receives user summaries from the Reckoner Services.
    '''
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/user?"
    if (active is False):
        url += "active=false&"
    if (active is True):
        url += "active=true&"
    if (sort_by):
        url += "sort_by=" + sort_by + "&" 
    if (ascending):
        url += "ascending=true" + "&"
    if (page is not None):
        url += "page=" + str(page) + "&" 
    if (size):
        url += "size=" + str(size) + "&" 
    if (session_id):
        url += "session_id=" + session_id + "&"
    
    response = urllib2.urlopen(url)
    content = response.read()
    servResponse = UserServiceResponse(xml_string = content)

    return servResponse 

def client_get_user_by_session(session_id):
    '''
    Receives the ID for the current session (as originally retrieved from
    the initial login - via OAuth or otherwise).  
    
    Checks the user token with the Reckoner Content Services and pulls the User
    information associated with the token.  Returns a UserServiceResponse object.
    '''
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/user/me"
    if (session_id):
        url += "?session_id=" + session_id
    
    response = urllib2.urlopen(url)
    content = response.read()
    servResponse = UserServiceResponse(xml_string = content)

    return servResponse 
    
    
def client_get_user_by_id(user_id, session_id):
    '''
    Receives the User ID (as stored in the Reckoner Database).  
    
    Pulls the User information associated with the ID.  Returns a UserServiceResponse object.
    '''
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/user/id/" + user_id
    if (session_id):
        url += "?session_id=" + session_id
    
    response = urllib2.urlopen(url)
    content = response.read()
    servResponse = UserServiceResponse(xml_string = content)

    return servResponse   

def client_update_user_permissions (permissionPost):
    '''
    Updates the user permissions as specified in the PermissionPost object.
    
    Returns a UserServiceResponse object.
    '''
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/user/permissions"

    req = urllib2.Request(url = url,
                          data = permissionPost.getXMLString(),
                          headers = {'Content-Type': 'text/xml'})
    
    response = urllib2.urlopen(req)
    content = response.read()
    servResponse = UserServiceResponse(xml_string = content)

    return servResponse  

def client_update_user (userPost, session_id):
    '''
    Updates the modifiable parts of the Reckoner user, as based on the received User object.
    
    Returns a UserServiceResponse object.
    '''
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/user/update"

    req = urllib2.Request(url = url,
                          data = userPost.getPostingXMLString(session_id),
                          headers = {'Content-Type': 'text/xml'})
    
    response = urllib2.urlopen(req)
    content = response.read()
    servResponse = UserServiceResponse(xml_string = content)

    return servResponse  

def client_get_permission_list ():
    '''
    Receives the list of permissions the Reckoner currently uses.
    '''
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/list/user/permissions"
    
    response = urllib2.urlopen(url)
    content = response.read()
    servResponse = DataServiceList(xml_string = content)

    return servResponse     

def client_get_group_list ():
    '''
    Receives the list of permissions the Reckoner currently uses.
    '''
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/list/user/groups"
    
    response = urllib2.urlopen(url)
    content = response.read()
    servResponse = DataServiceList(xml_string = content)

    return servResponse          