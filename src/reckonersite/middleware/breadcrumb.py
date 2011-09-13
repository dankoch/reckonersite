'''
Created on Sep 6, 2011
@author: danko
'''

import logging
import traceback
import uuid

from django.conf import settings

logger = logging.getLogger(settings.STANDARD_LOGGER)

class BreadcrumbMiddleware(object):
    
    def process_request(self, request):
        '''
        Tracks the last site the user has viewed as a reference for things like login
        and other activities where the user should be redirected back to a previously viewed
        site.  Sites that should NOT be breadcrumbed are noted in 'EXEMPT_URLS'
        '''
        EXEMPT_URLS = ('/login', '/static', '/favicon', )
        
        currentBreadcrumb = request.session.get(settings.LAST_SITE_TOKEN_ID, None)

        if (request.get_full_path().startswith(EXEMPT_URLS)):
            return None
            
        request.session[settings.LAST_SITE_TOKEN_ID] = request.get_full_path()        