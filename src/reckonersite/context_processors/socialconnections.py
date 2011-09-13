'''
Created on Sep 8, 2011
@author: danko
'''

import logging
from django.conf import settings

logger = logging.getLogger(settings.STANDARD_LOGGER)

def set_social_info(request):

    social_info = {'FACEBOOK_OAUTH_URL' : settings.FACEBOOK_OAUTH_URL,
                   'FACEBOOK_APP_ID' : settings.FACEBOOK_APP_ID,
                   'FACEBOOK_REDIRECT_URL' : settings.FACEBOOK_REDIRECT_URL,
                   'FACEBOOK_SCOPE' : settings.FACEBOOK_SCOPE,
                   'GOOGLE_API_OAUTH_URL' : settings.GOOGLE_API_OAUTH_URL,
                   'GOOGLE_APP_ID' : settings.GOOGLE_APP_ID,
                   'GOOGLE_REDIRECT_URL' : settings.GOOGLE_REDIRECT_URL,
                   'GOOGLE_SCOPE' : settings.GOOGLE_SCOPE}
    
    return social_info