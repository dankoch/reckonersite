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

from reckonersite.client.authclient import client_authenticate_user, \
                                           client_logout_user, \
                                           client_get_user_by_session, \
                                           client_get_user_by_id, \
                                           client_update_user_permissions, \
                                           client_get_group_list
from reckonersite.domain.base import convertToDateTime
from reckonersite.domain.oauthaccesstoken import OAuthAccessToken
from reckonersite.domain.permissionpost import PermissionPost
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
    siteUser = None
    
    if (oAuthReceipt):
        authResponse = client_authenticate_user(oAuthReceipt)
    
    if (authResponse):
        if ((not authResponse.status.success) or (not authResponse.reckoner_user)):
            # For invalid Google Accounts (i.e. non G+ Google Accounts), mark the user
            # and return to the view.  Otherwise, return None and the view will handle it.
            if (authResponse.status.message == "R707_AUTH_USER"):
                siteUser = SiteCustomUser(is_invalid_google_user=True)
                return siteUser
            
            logger.warning('Failed to authenticate user against Reckoner Services: ' \
                           + authResponse.status.message)
            return None
        else:
            siteUser = SiteCustomUser(reckoner_user = authResponse.reckoner_user, 
                                        auth_session = authResponse.auth_session)

    return siteUser
  

def get_user(session_id, user_id=None):
    '''
    Retrieves the user information associated with the specified session ID or user ID.
    '''
    siteUser = None
    
    if (user_id):
        userResponse = client_get_user_by_id(user_id, session_id)
    else:
        userResponse = client_get_user_by_session(session_id)
        
    if (userResponse):
        if ((not userResponse.status.success) or (not userResponse.reckoner_user)):
            logger.warning('Failed to retrieve user from Reckoner Services: ' \
                           + userResponse.status.message)
            return None
        else:
            if (userResponse.auth_session):
                siteUser = SiteCustomUser(reckoner_user = userResponse.reckoner_user, 
                                          auth_session = userResponse.auth_session) 
            else:
                siteUser = SiteCustomUser(reckoner_user = userResponse.reckoner_user)                   
                siteUser.session_id = session_id
               
    return siteUser
    

def logout_user(session_id):
    '''
    Deletes the session information from the Reckoner Services when the user ends their
    Reckoner Site session.
    '''
    servResponse = client_logout_user(session_id)
    if not servResponse.status.success:
        logger.error("Received Reckoner Service error when logging out session ID: " + \
                      session_id + ":" + servResponse.status.message)
    else:
        logger.debug("Logged out user " + session_id)
        

def change_user_permissions(action, group, active, user_id, session_id):
    '''
    Changes the user permissions per the specified information.
    
    'action' must be 'ADD', 'REMOVE', or 'REPLACE'
    'groups' is a list of Groups to have the user join.
    'active' is whether the user should be active or not.
    'user_id' is the ID of the user changing their ID
    'session_id' is the session  ID of user requesting the change
    '''
    
    permissionPost = PermissionPost(action, group, active, user_id, session_id)
    
    servResponse = client_update_user_permissions(permissionPost)
    if not servResponse.status.success:
        logger.error("Received Reckoner Service error when logging out session ID: " + \
                      session_id + ":" + servResponse.status.message)
    else:
        logger.debug("Logged out user " + session_id)


def get_group_list():
    '''
    Gets the list of groups a user can belong to.
    '''
    servResponse = client_get_group_list()
    if not servResponse.status.success:
        logger.error("Received Reckoner Service error when getting group list: " + \
                      ":" + servResponse.status.message)
    else:
        logger.debug("Got group list.")            
    
    return servResponse.data