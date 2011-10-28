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
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from reckonersite.client.authclient import client_get_user_by_id
from reckonersite.client.commentclient import client_get_user_comments, client_get_favorited_comments
from reckonersite.client.reckoningclient import client_get_user_reckonings, client_get_favorited_reckonings
from reckonersite.client.voteclient import client_get_user_reckoning_votes

from reckonersite.util.validation import purgeHtml, sanitizeDescriptionHtml, sanitizeCommentHtml
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
    
