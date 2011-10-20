'''
Created on Aug 23, 2011
@author: danko
'''
import logging
import sys
import traceback

from django.conf import settings
from django.http import HttpResponse

from reckonersite.client.noteclient import client_post_reckoning_favorite, \
                                           client_post_reckoning_flag, \
                                           client_post_reckoning_comment_favorite, \
                                           client_post_reckoning_comment_flag 

from reckonersite.domain.ajaxserviceresponse import AjaxServiceResponse
from reckonersite.domain.favorite import Favorite
from reckonersite.domain.flag import Flag

logger = logging.getLogger(settings.STANDARD_LOGGER)


###############################################################################################
## The endpoint responsible for posting a favorite to a reckoning 
#  (as used primarily for AJAX calls).
###############################################################################################

def post_reckoning_favorite(request, id = None):
    
    site_response = None
    
    try:
        if request.method == 'POST':
            if (id):
                favorite = Favorite(user_id = request.user.reckoner_id)
                service_response = client_post_reckoning_favorite(favorite, id, request.user.session_id)
                
                if (service_response.success):
                    site_response = AjaxServiceResponse(success=True,
                                                        message="success",
                                                        message_description="Tracked!")
                elif (service_response.message == "R805_POST_NOTE"):
                    site_response = AjaxServiceResponse(success=False,
                                                        message="self-fave",
                                                        message_description="This is your own reckoning.")
                elif (service_response.message == "R804_POST_NOTE"):
                    site_response = AjaxServiceResponse(success=False,
                                                    message="self-fave",
                                                    message_description="Already tracking!")
                else:
                    site_response = AjaxServiceResponse(success=False,
                                                    message="whoops", 
                                                    message_description='Sorry!')
                                
                
    except Exception:
        logger.error("Exception when favoriting a reckoning:") 
        logger.error(traceback.print_exc(8))    
        site_response = AjaxServiceResponse(success=False,
                                            message="whoops", 
                                            message_description='No go. Try again later.')

    return HttpResponse(site_response.getXMLString())

###############################################################################################
## The endpoint responsible for posting a flag to a reckoning 
#  (as used primarily for AJAX calls).
###############################################################################################

def post_reckoning_flag(request, id = None):
    
    site_response = None
    
    try:
        if request.method == 'POST':
            if (id):
                flag = Flag(user_id = request.user.reckoner_id)
                service_response = client_post_reckoning_flag(flag, id, request.user.session_id)
                
                if (service_response.success):
                    site_response = AjaxServiceResponse(success=True,
                                                        message="success",
                                                        message_description="Flagged!")
                elif (service_response.message == "R805_POST_NOTE"):
                    site_response = AjaxServiceResponse(success=False,
                                                        message="self-flag",
                                                        message_description="Self-flaggelation!")
                elif (service_response.message == "R804_POST_NOTE"):
                    site_response = AjaxServiceResponse(success=False,
                                                    message="self-flag",
                                                    message_description="Already flagged!")
                else:
                    site_response = AjaxServiceResponse(success=False,
                                                    message="whoops", 
                                                    message_description='Sorry!')
                                
                
    except Exception:
        logger.error("Exception when flagging a reckoning:") 
        logger.error(traceback.print_exc(8))    
        site_response = AjaxServiceResponse(success=False,
                                            message="whoops", 
                                            message_description='No go. Try again later.')

    return HttpResponse(site_response.getXMLString())

###############################################################################################
## The endpoint responsible for posting a favorite to a reckoning comment
#  (as used primarily for AJAX calls).
###############################################################################################

def post_reckoning_comment_favorite(request, id = None):
    
    site_response = AjaxServiceResponse(success=False,
                                        message="whoops", 
                                        message_description='No go. Try again later.')

    
    if (request.user.has_perm('FAVORITE')):
        try:
            if request.method == 'POST':
                favorite = Favorite(user_id = request.user.reckoner_id)
                service_response = client_post_reckoning_comment_favorite(favorite, 
                                                                          id, 
                                                                          request.user.session_id)

                if (service_response.success):
                    site_response = AjaxServiceResponse(success=True,
                                                        message="success",
                                                        message_description="Favorited!")
                elif (service_response.message == "R805_POST_NOTE"):
                    site_response = AjaxServiceResponse(success=False,
                                                        message="self-fave",
                                                        message_description="This is your own comment!")
                elif (service_response.message == "R804_POST_NOTE"):
                    site_response = AjaxServiceResponse(success=False,
                                                    message="duplicate",
                                                    message_description="Already favorited this one!")                              
                
        except Exception:
            logger.error("Exception when favoriting a reckoning:") 
            logger.error(traceback.print_exc(8))    

    
    return HttpResponse(site_response.getXMLString())


###############################################################################################
## The endpoint responsible for posting a favorite to a reckoning comment
#  (as used primarily for AJAX calls).
###############################################################################################

def post_reckoning_comment_flag(request, id = None):
    
    site_response = AjaxServiceResponse(success=False,
                                        message="whoops", 
                                        message_description='No go. Try again later.')

    
    if (request.user.has_perm('FLAG')):
        try:
            if request.method == 'POST':

                flag = Flag(user_id = request.user.reckoner_id)
                service_response = client_post_reckoning_comment_flag(flag, 
                                                                      id, 
                                                                      request.user.session_id)

                print ("Comment Flag: " + site_response.getXMLString())                                
                
                if (service_response.success):
                    site_response = AjaxServiceResponse(success=True,
                                                        message="success",
                                                        message_description="Flagged! Reckonbot is on it!")
                elif (service_response.message == "R805_POST_NOTE"):
                    site_response = AjaxServiceResponse(success=False,
                                                        message="self-fave",
                                                        message_description="Self-flagellation!")
                elif (service_response.message == "R804_POST_NOTE"):
                    site_response = AjaxServiceResponse(success=False,
                                                    message="duplicate",
                                                    message_description="Already flagged this one!")  
                
        except Exception:
            logger.error("Exception when flagging a reckoning:") 
            logger.error(traceback.print_exc(8))    

    
    return HttpResponse(site_response.getXMLString())