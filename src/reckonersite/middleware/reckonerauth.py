'''
Created on Sep 6, 2011
@author: danko
'''

import logging
import traceback
import uuid

from django.conf import settings

from reckonersite.auth import reckonerauthbackend
from reckonersite.domain.anonsitecustomuser import AnonSiteCustomUser
from reckonersite.domain.sitecustomuser import SiteCustomUser

logger = logging.getLogger(settings.STANDARD_LOGGER)

def get_user(request, session_id):
    if not hasattr(request, '_cached_user'):
        request._cached_user = reckonerauthbackend.get_user(session_id)
    return request._cached_user   

def logout_user(request, session_id):
    reckonerauthbackend.logout_user(session_id)
    request.session.flush()
    if hasattr(request, '_cached_user'):
        del request._cached_user 

class ReckonerAuthMiddleware(object):
    
    def process_request(self, request):
        
        # Check the session to see if a user token is specified.
        if (request.session.get(settings.RECKONER_API_SESSION_ID, None)):
            
        # Check the Token ID to see if it's anonymous (i.e. starts w/ 'anon_')
        # If so, create an AnonSiteCustomUser as request.user and move along.
        # Otherwise, use the token to extract the user credentials from the Reckoner
        # Services.  
        #
        # If none comes back, the session is dead - log the user out by 
        # by clearing their session and cleaning up the Reckon Services
            session_id = request.session.get(settings.RECKONER_API_SESSION_ID, None)       
            try:
                if (session_id.startswith('anon_')):
                    request.user = AnonSiteCustomUser(session_id)
                else:
                    # Retrieve the user permissions and store in the request.
                    # If nothing is retrieved, log the user out.
                    # If the retrieved user has a session id, make the stored session ID matches.
                    
                    request.user = get_user(request, session_id)
                    if (not request.user):
                        logout_user(request, session_id)
                    elif (request.user.session_id):
                        request.session[settings.RECKONER_API_SESSION_ID] = request.user.session_id
                    else:
                        request.user.session_id = request.session[settings.RECKONER_API_SESSION_ID]

            except Exception:
                logger.warning('Exception when retrieving user: ' + session_id)
                logger.error(traceback.print_exc(8))
                logout_user(request, session_id)
                
        # If the Session Token ID is None (either because it's a new user, or it just
        # got flushed out), create a new one and log the user in as anonymous.
        if (not request.session.get(settings.RECKONER_API_SESSION_ID, None)):
            request.session[settings.RECKONER_API_SESSION_ID] = "anon_" + str(uuid.uuid4())
            request.user = AnonSiteCustomUser(request.session.get(settings.RECKONER_API_SESSION_ID, None))

        