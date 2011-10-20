'''
Created on Sep 6, 2011
@author: danko
'''

import logging
from django.conf import settings

logger = logging.getLogger(settings.STANDARD_LOGGER)


def set_reckoning_context(request):
    
    site_context = {'SITE_ROOT' : settings.SITE_ROOT,
                    'SITE_NAME' : settings.SITE_NAME}
    
    return site_context