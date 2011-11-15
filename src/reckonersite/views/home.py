'''
Created on Aug 31, 2011

@author: danko
'''
import logging
import sys
import traceback

from django import forms
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from reckonersite.client.reckoningclient import client_get_reckonings, \
                                                client_get_open_reckonings, \
                                                client_get_closed_reckonings

from reckonersite.views.vote import post_reckoning_vote, get_user_reckoning_vote
from reckonersite.util.math import computeReckoningAnswerPercentages

logger = logging.getLogger(settings.STANDARD_LOGGER)

def home_page(request):
    errors={}
    
    try:    
        if request.method == 'POST':
            if 'postvote' in request.POST:
                if (request.user.has_perm('VOTE')):
                    if ('answer' in request.POST):
                        errors.update(post_reckoning_vote(request))
        
        reckoning = None
        user_vote = None
        highlighted_response = client_get_reckonings(sort_by="postingDate",
                                                     page="0", size="1",
                                                     highlighted=True, 
                                                     session_id=request.user.session_id)
        if (highlighted_response.reckonings):
            reckoning = computeReckoningAnswerPercentages(highlighted_response.reckonings[0])
            user_vote = get_user_reckoning_vote(request, reckoning.id)

        recent_reckoning_response = client_get_open_reckonings(page="0", size="4", 
                                                               session_id=request.user.session_id)
        
        popular_reckoning_response = client_get_open_reckonings(sort_by="views",
                                                               page="0", size="4", 
                                                               session_id=request.user.session_id)        
        
        last_call_response = client_get_open_reckonings(sort_by="closingDate", ascending=True,
                                                        page="0", size="4", 
                                                        session_id=request.user.session_id)
        
        recent_finished_response = client_get_closed_reckonings(sort_by="closingDate", ascending=False,
                                                                page="0", size="4", 
                                                                session_id=request.user.session_id)
        
        c = RequestContext(request, {'reckoning' : reckoning,
                                     'popular_reckonings' : popular_reckoning_response.reckonings,
                                     'recent_reckonings' : recent_reckoning_response.reckonings,
                                     'last_call_reckonings' : last_call_response.reckonings,
                                     'finished_reckonings' : recent_finished_response.reckonings,
                                     'user_vote' : user_vote,
                                     'errors' : errors})
        
        return render_to_response('index.html', c)
            
    except Exception:      
        logger.error("Exception when rending home page:") 
        logger.error(traceback.print_exc(8))
        raise Exception
    
    
def search_page(request):
    return render_to_response('search.html', RequestContext(request, None))