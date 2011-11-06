'''
Created on Aug 23, 2011
@author: danko
'''
import logging
import sys
import traceback

from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from reckonersite.client.authclient import client_get_user_by_id, client_update_user
from reckonersite.client.commentclient import client_get_user_comments, client_get_favorited_comments
from reckonersite.client.reckoningclient import client_get_user_reckonings, client_get_favorited_reckonings
from reckonersite.client.voteclient import client_get_user_reckoning_votes

from reckonersite.domain.ajaxserviceresponse import AjaxServiceResponse
from reckonersite.domain.reckoneruser import ReckonerUser
from reckonersite.domain.userajaxresponse import UserAjaxResponse

from reckonersite.util.validation import purgeHtml, sanitizeDescriptionHtml, sanitizeCommentHtml, sanitizeBioHtml
from reckonersite.util.pagination import pageDisplay

logger = logging.getLogger(settings.STANDARD_LOGGER)

    
###############################################################################################
# The page responsible for showing a list of current open reckonings
###############################################################################################


def get_user_profile(request, id = None, name = None):

    try:        
        # Check to see if we're coming here from a GET.  If so, we've got work to do.
        if request.method == 'GET':
            
            service_response = client_get_user_by_id(id, request.user.session_id)
            
            if (not service_response.status.success):
                logger.warning("Error when retrieving user profile: " + service_response.status.message)
                raise BaseException() 
            elif (not service_response.reckoner_user):
                raise Http404
            elif (request.path != service_response.reckoner_user.getURL()):
                return HttpResponseRedirect(service_response.reckoner_user.getURL())
            else:         
                page_url = service_response.reckoner_user.getURL()
                             
                # Pull the relevant variables from the request string.
                page = request.GET.get('page', "1")
                size = request.GET.get('size', None)
                tab = request.GET.get('tab', None)
                
                # Persist the specified variables in the session for when the user navigates away and back.
                # Otherwise, pull the information out of the session                    
                if (size):
                    request.session['user-size'] = size
                else:
                    size = request.session.get('user-size', '15')         
                    
                if (tab):
                    request.session['user-tab'] = tab
                else:
                    tab = request.session.get('user-tab', 'newest') 
                
                reckonings_response = client_get_user_reckonings(id, int(page)-1, size, request.user.session_id)
                comments_response = client_get_user_comments(id, int(page)-1, size, request.user.session_id)
                votes_response = client_get_user_reckoning_votes(id, int(page)-1, size, request.user.session_id)
                tracking_response = client_get_favorited_reckonings(id, int(page)-1, size, request.user.session_id)
                
                # Execute the correct action based on the selected tab and info.  Valid tabs:
                #  * tracking, comments, votes, reckonings
                if (tab == "tracking"):
                    total_count = tracking_response.count
                    reckonings = tracking_response.reckonings
                elif (tab == "comments"):
                    total_count = comments_response.count                    
                    reckonings = comments_response.reckonings
                elif (tab == "votes"):
                    total_count = votes_response.count                    
                    reckonings = votes_response.reckonings
                    
                else:
                    tab = 'reckonings'
                    total_count = reckonings_response.count
                    reckonings = reckonings_response.reckonings
                            
                context = {'profile_user' : service_response.reckoner_user,
                           'reckonings' : reckonings,
                           'page' : int(page),
                           'size' : int(size),
                           'tab'  : tab,
                           'page_url' : page_url,
                           'reckoning_count' : reckonings_response.count,
                           'comment_count' : comments_response.count,
                           'vote_count' : votes_response.count,
                           'tracking_count' : tracking_response.count}
                
                context.update(pageDisplay(page, size, total_count))
                c = RequestContext(request, context)
            
                return render_to_response('user_profile.html', c)
    except Exception:
        logger.error("Exception when showing a user profile:") 
        logger.error(traceback.print_exc(8))
        raise Exception         


###############################################################################################
#  The endpoint responsible for updating a user's bio upon submission.
#  (as used primarily for AJAX calls)
###############################################################################################

def update_reckoning_bio(request, id = None):
    site_response = AjaxServiceResponse(success=False,
                                        message="whoops", 
                                        message_description='No go. Try again later.')
    
    if (request.user.has_perm('UPDATE_PROFILE_INFO') or id == request.user.reckoner_id):
        try:
            if request.method == 'POST':
                bio = sanitizeBioHtml(request.POST.get("user-bio", ""))
                
                if (len(bio) > 1000):
                    site_response = AjaxServiceResponse(success=False,
                                                        message="too_long",
                                                        message_description="Maximum Length is 1000 Characters (minus markup)")
                else: 
                    userUpdate = ReckonerUser(id=id, bio=bio)
                    service_response = client_update_user(userUpdate,
                                                          request.user.session_id)                              
                    
                    if (service_response.status.success):
                        site_response = AjaxServiceResponse(success=True,
                                                            message="success",
                                                            message_description="Updated!")
                
        except Exception:
            logger.error("Exception when flagging a reckoning:") 
            logger.error(traceback.print_exc(8))    

    
    return HttpResponse(site_response.getXMLString())


###############################################################################################
#  The endpoint responsible for getting user info
#  (as used primarily for AJAX calls)
###############################################################################################

def get_user_info_ajax(request, id = None):
    site_response = AjaxServiceResponse(success=False,
                                        message="whoops", 
                                        message_description='No go. Try again later.')
    
    if (request.user.has_perm('VIEW_PROFILE') or id == request.user.reckoner_id):
        try:
            if request.method == 'GET':
                service_response = client_get_user_by_id(id, request.user.session_id)
                
                if (not service_response.status.success):
                    logger.warning("Error when retrieving user profile: " + service_response.status.message)
                elif (not service_response.reckoner_user):
                    site_response = AjaxServiceResponse(success=False,
                        message="not found", 
                        message_description='No user by that ID.')
                else:
                    site_response = UserAjaxResponse(success=True,
                        message="Success.", 
                        message_description='Success!',
                        reckoner_user=service_response.reckoner_user)
                    
            print site_response.getXMLString()
                
        except Exception:
            logger.error("Exception when getting a user:") 
            logger.error(traceback.print_exc(8))    

    return HttpResponse(site_response.getXMLString())
