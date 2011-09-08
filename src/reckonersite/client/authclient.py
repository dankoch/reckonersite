'''
Created on Aug 25, 2011
@author: danko
'''
import urllib2

from django.conf import settings
from reckonersite.domain.authsession import AuthSession
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

def client_logout_user(user_token):
    '''
    Receives the user token for the current session (as originally retrieved from
    the initial login - via OAuth or otherwise).  
    
    Forwards this information to the Reckoner Content Services, which deletes the associated
    session and logs the user out.
    '''
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/user/logout" + "?user_token=" + user_token
    
    response = urllib2.urlopen(url)
    content = response.read()
    servResponse = UserServiceResponse(xml_string = content)

    return servResponse 

def client_get_user(user_token):
    '''
    Receives the user token for the current session (as originally retrieved from
    the initial login - via OAuth or otherwise).  
    
    Checks the user token with the Reckoner Content Services and pulls the User
    information associated with the token.  Returns a UserServiceResponse object.
    '''
    url = settings.RECKON_CONTENT_SERVICES_HOST + "/user/me" + "?user_token=" + user_token
    
    response = urllib2.urlopen(url)
    content = response.read()
    servResponse = UserServiceResponse(xml_string = content)

    return servResponse 
    
    
        