'''
Created on Aug 23, 2011
@author: danko
'''
import logging
import traceback

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

from reckonersite.client.contentclient import client_get_contents

from reckonersite.domain.ajaxserviceresponse import AjaxServiceResponse
from reckonersite.domain.contentajaxresponse import ContentAjaxResponse

logger = logging.getLogger(settings.STANDARD_LOGGER)
    
    
###############################################################################################
#  The endpoint for retrieving the most recent blog posts for the sidebar
#  (as used primarily for AJAX calls)
###############################################################################################

@cache_page(60 * 15)
def get_recent_blog_ajax(request, id = None):
    site_response = AjaxServiceResponse(success=False,
                                        message="whoops", 
                                        message_description='No go. Try again later.')
    
    if (request.user.has_perm('VIEW_CONTENT')):
        try:
            if request.method == 'GET':          
                size = request.GET.get("size", "1")
                
                service_response = client_get_contents(type="BLOG", page=0, size=int(size),
                                                    sort_by="postingDate", ascending=False)
                                       
                if (service_response.status.success):
                    site_response = ContentAjaxResponse(contents=service_response.contents,
                                                          success=service_response.status.success)

                else:
                    logger.error("Error when retrieving recent blog posts: " + service_response.status.message)
                
        except Exception:
            logger.error("Exception when retrieving recent blog posts:") 
            logger.error(traceback.print_exc(8))    

    return HttpResponse(site_response.getXMLString())