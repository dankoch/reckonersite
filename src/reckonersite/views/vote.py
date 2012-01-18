'''
Created on Aug 23, 2011
@author: danko
'''
import logging
import sys
import traceback

from django.conf import settings
from django.http import HttpResponse

from reckonersite.client.voteclient import client_post_reckoning_vote, \
                                           client_get_user_reckoning_vote, \
                                           client_update_reckoning_vote

from reckonersite.domain.ajaxserviceresponse import AjaxServiceResponse
from reckonersite.domain.vote import Vote

logger = logging.getLogger(settings.STANDARD_LOGGER)


###############################################################################################
# The endpoint responsible for posting a vote and returning the corresponding error
# dictionary.
###############################################################################################

def post_reckoning_vote(request):
    errors={'vote_error' : True}
    
    try:
        # Check to see if we're coming here from a POST.  If so, we've got work to do.
        if request.method == 'POST':
            if (request.user.has_perm('VOTE')):
                if ('answer' in request.POST):
                    vote = Vote(voter_id=request.user.reckoner_id,
                                answer_index=request.POST.get('answer', None),
                                anonymous=request.user.is_anonymous,
                                ip=request.META.get('REMOTE_ADDR', None),
                                user_agent=request.META.get('HTTP_USER_AGENT', None))
                    
                    vote_service_response = client_post_reckoning_vote(vote, request.POST.get('id'), 
                                                                       request.POST.get('answer'), 
                                                                       request.user.reckoner_id)
                    # If the vote update failed, check to see if it's the error code that corresponds
                    # with a suspected duplicate vote.  If so, mark it as such.
                    if not vote_service_response.success:
                        if (vote_service_response.message == "R602_POST_VOTE"):
                            errors["phony_vote"]=True

                        logger.info("Invalid vote submitted: " + request.POST.get('id') + " " + request.POST.get('answer') + \
                                    " " + request.user.reckoner_id + " " + unicode(request.META.get('REMOTE_ADDR', None)) +
                                    " " + vote_service_response.message)
                    else:
                        errors['vote_error'] = False

    except Exception:
        logger.error("Exception when showing a reckoning:") 
        logger.error(traceback.print_exc(8))
        raise Exception  
    
    return errors
    
    
def get_user_reckoning_vote(request, id=None):
    '''
    Retrieves the user's vote for the specified Reckoning ID.  Accepts "reckoning_id" for GET requests,
    or the id parameter for direct requests from other controllers.
    
    Returns object of type reckonsite.domain.vote
    '''
    # Pull the user's vote for this reckoning and add it to the context.
    user_vote = None
    
    if not id:
        id = request.GET.get("reckoning_id", None)
    
    if (id):
        user_vote_response = client_get_user_reckoning_vote(id, request.user.reckoner_id, request.user.session_id)
        if (not user_vote_response.status.success):
            user_vote = Vote(answer_index=-1)
            logger.error(user_vote_response.status.message)
        else:
            if (user_vote_response.votes):
                user_vote = user_vote_response.votes[0]
        
    return user_vote


###############################################################################################
#  The endpoint responsible for updating a vote.
#  (as used primarily for AJAX calls)
###############################################################################################

def update_reckoning_vote(request, reckoning_id = None, user_id = None, answer_index = None):
    site_response = AjaxServiceResponse(success=False,
                                        message="whoops", 
                                        message_description='No go. Try again later.')
    
    if (request.user.has_perm('UPDATE_PROFILE_INFO') or user_id == request.user.reckoner_id):
        try:
            if request.method == 'POST':
                anonymous = request.POST.get("anonymous", None)
                if (anonymous is not None):
                    anonymous = (anonymous == 'true')
                
                if (reckoning_id and user_id and answer_index): 
                    voteUpdate = Vote(voter_id=user_id, reckoning_id=reckoning_id,
                                         answer_index=answer_index, anonymous=anonymous)
                    
                    service_response = client_update_reckoning_vote(voteUpdate,
                                                          request.user.session_id)                    
                    
                    if (service_response.success):
                        site_response = AjaxServiceResponse(success=True,
                                                            message="success",
                                                            message_description="Updated!")
                
        except Exception:
            logger.error("Exception when updating a reckoning vote:") 
            logger.error(traceback.print_exc(8))    

    
    return HttpResponse(site_response.getXMLString())