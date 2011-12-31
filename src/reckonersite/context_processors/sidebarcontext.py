'''
Created on Sep 8, 2011
@author: danko
'''

import logging
from django.conf import settings

from reckonersite.client.contentclient import client_get_contents

logger = logging.getLogger(settings.STANDARD_LOGGER)

def set_podcast_info(request):
    '''
    Used to ensure the latest podcast is always available for the sidebar in
    the Django templates.  If the sidebar DOESN'T INCLUDE THE LATEST PODCAST,
    DELETE THIS.  There is no reason to make the call if not necessary.
    '''

    content_list_response = client_get_contents(type = "PODCAST",
                                                page=0, size=1, 
                                                sort_by="postingDate", ascending=False)

    if (content_list_response.contents):
        content = content_list_response.contents[0]
    else:
        content = None
    
    return {'last_podcast' : content}