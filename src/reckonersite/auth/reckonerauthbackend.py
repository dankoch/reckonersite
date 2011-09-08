'''
Created on Sep 4, 2011
@author: danko
'''
import logging
import sys
import traceback
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_out

from reckonersite.client.authclient import client_authenticate_user, client_logout_user, client_get_user
from reckonersite.domain.base import convertToDateTime
from reckonersite.domain.oauthaccesstoken import OAuthAccessToken
from reckonersite.domain.sitecustomuser import SiteCustomUser

logger = logging.getLogger(settings.STANDARD_LOGGER)

def authenticate(oAuthReceipt = None, username = None, password = None):
    '''
    Authenticate against the Reckoner Content Services using a User Token retrieved from an 
    OAUTH provider.
    
    Supply the OAUTH token provided by the OAUTH provider (as an OAuthAccessToken).
    Returns a ReckonerUser object, as provided by the service.
    Username and password are also included as arguments, but not currently supported.
    '''
    djangoUser = None
    
    if (oAuthReceipt):
        authResponse = client_authenticate_user(oAuthReceipt)
    
    if (authResponse):
        if ((not authResponse.status.success) or (not authResponse.reckoner_user)):
            logger.warning('Failed to authenticate user against Reckoner Services: ' \
                           + authResponse.status.message)
            return None
        else:
            siteUser = SiteCustomUser(reckoner_user = authResponse.reckoner_user, 
                                        auth_session = authResponse.auth_session)

    return siteUser
  

def get_user(user_token):
    '''
    Retrieves the user information associated with the specified user token.
    '''
    siteUser = None
    
    if (user_token):
        userResponse = client_get_user(user_token)
        if (userResponse):
            if ((not userResponse.status.success) or (not userResponse.reckoner_user)):
                logger.warning('Failed to retrieve user from Reckoner Services: ' \
                               + userResponse.status.message)
                return None
            else:
                siteUser = SiteCustomUser(reckoner_user = userResponse.reckoner_user)
                siteUser.user_token = user_token
               
    return siteUser
    

def logout_user(user_token):
    '''
    Deletes the session information from the Reckoner Services when the user ends their
    Reckoner Site session.
    '''
    servResponse = client_logout_user(user_token)
    if not servResponse.status.success:
        logger.error("Received Reckoner Service error when logging out user token " + \
                      user_token + ":" + servResponse.status.message)
    else:
        logger.debug("Logged out user " + user_token)        
        