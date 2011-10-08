'''
Created on Sep 6, 2011
@author: danko
'''

import logging
from django.conf import settings

logger = logging.getLogger(settings.STANDARD_LOGGER)

def set_user_info(request):
    user_info = None
    
    if (request.user):
        user_info = {'user' : request.user, 'perms' : request.user.permissions}
    
    return user_info