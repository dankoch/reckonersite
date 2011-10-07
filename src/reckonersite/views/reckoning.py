'''
Created on Aug 23, 2011
@author: danko
'''
import logging
import sys
import traceback

from django import forms
from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from reckonersite.client.reckoningclient import client_get_reckoning, client_post_reckoning
from reckonersite.client.voteclient import client_get_user_reckoning_vote
from reckonersite.domain.answer import Answer
from reckonersite.domain.reckoning import Reckoning
from reckonersite.domain.vote import Vote
from reckonersite.util.math import computeReckoningAnswerPercentages
from reckonersite.util.validation import purgeHtml, sanitizeFreeTextHtml, slugifyTitle

logger = logging.getLogger(settings.STANDARD_LOGGER)


###############################################################################################
# The page responsible for the actual submission of new Reckonings.
###############################################################################################


def post_reckoning(request):
      
    try:
        # Check to see if we're coming here from a POST.  If so, process it.  If not, give 'em a fresh form.
        if request.method == 'POST' :
            form = PostReckoningForm(request.POST)
            
            # Check form validation -- kick the form back out with error messages if failed.
            if form.is_valid():
                answers = [Answer(index=0), Answer(index=1)]
                for key, attr in form.cleaned_data.iteritems():
                    if (key.startswith("answer")):
                        index = key.split('_')[1]
                        answers[int(index)-1].text = purgeHtml(attr)
                    elif (key.startswith("subtitle")):
                        index = key.split('_')[1]
                        answers[int(index)-1].subtitle = purgeHtml(attr)

                reckoning=Reckoning(question=purgeHtml(form.cleaned_data['question']),
                                    description=sanitizeFreeTextHtml(form.cleaned_data['description']),
                                    answers=answers,
                                    tag_csv=purgeHtml(form.cleaned_data['tags']),
                                    submitter_id=request.user.reckoner_id)
            
                # Submit to the API
                response = client_post_reckoning(reckoning, request.user.session_id)
                
                # Check to see if the API submission was a success.  If not, clean the error and display.  Otherwise, great!
                if not response.success:
                    logger.error("Error from post attempt: " + response.message)
                    raise Exception
                else:                    
                    return HttpResponseRedirect('/thanks-for-playing')
        else :
            form = PostReckoningForm()
        
        c = RequestContext(request,{'form' : form,})
        return render_to_response('post-reckoning.html', c)
    except Exception:      
        logger.error("Exception when showing and processing the Submit-a-Reckoning form:") 
        logger.error(traceback.print_exc(8))
        raise Exception        

class PostReckoningForm(forms.Form):  
    question = forms.CharField(max_length=150, label="Question", required=True, widget=forms.Textarea)
    description = forms.CharField(max_length=1000, label="Description", required=False, widget=forms.Textarea)
    
    answer_1 = forms.CharField(max_length=25, label="Answer 1", required=True)
    subtitle_1 = forms.CharField(max_length=25, label="Subtitle 1", required=False)
    answer_2 = forms.CharField(max_length=25, label="Answer 2", required=True)
    subtitle_2 = forms.CharField(max_length=25, label="Subtitle 2", required=False)

    tags = forms.CharField(max_length=100, label="Tags", required=False)


###############################################################################################
# The page welcomes people who are attempting to post a reckoning.
###############################################################################################

def post_reckoning_welcome(request):
    
    return render_to_response('post-reckoning-welcome.html', RequestContext(request, None))


###############################################################################################
# The page responsible for thanking users who have posted a Reckoning.
###############################################################################################

def post_reckoning_thanks(request):
    
    return render_to_response('post-reckoning-thanks.html', RequestContext(request, None))


def get_reckoning(request, id = None, title = None):
    try:
        service_response = client_get_reckoning(id, "none")
        
        # Check to see if the API submission was a success.  If not, straight to the fail-page!
        # If the Reckoning list is empty, there's no Reckoning by that ID.  Straight to the 404 page!
        # If the passed title doesn't match the slugified question matching the ID, redirect so that it does.
        if (not service_response.status.success):
            raise BaseException() 
        elif (not service_response.reckonings):
            raise Http404
        elif (slugifyTitle(service_response.reckonings[0].question) != title):
            return HttpResponseRedirect('/reckoning/' + id + "/" + slugifyTitle(service_response.reckonings[0].question))
        else:            
            reckoning = computeReckoningAnswerPercentages(service_response.reckonings[0])
            leader = None
            
            # Pull the user's vote for this reckoning and add it to the context.
            user_vote_response = client_get_user_reckoning_vote(id, request.user.reckoner_id, request.user.session_id)
            user_vote = None
            if (not user_vote_response.status.success):
                logger.error(user_vote_response.status.message)
                user_vote = Vote(answer_index=-1)
            else:
                if (user_vote_response.votes):
                    user_vote = user_vote_response.votes[0]
            
            # Compute which answer has received the most votes as an index (-1 meaning a tie)
            if (reckoning.answers[0].vote_total > reckoning.answers[1].vote_total):
                leader = 0
            elif (reckoning.answers[0].vote_total < reckoning.answers[1].vote_total):
                leader = 1
            else:
                leader = -1
            
            c = RequestContext(request, {'reckoning' : reckoning,
                                         'user_vote' : user_vote,
                                         'leader' : leader,
                                         'time_remaining' : reckoning.getRemainingTime()})
            
            return render_to_response('reckoning.html', c)
    except Http404:
        logger.debug("Received 404 looking for page: " + request.get_full_path())
        raise Http404
    except Exception:
        logger.error("Exception when showing a reckoning:") 
        logger.error(traceback.print_exc(8))
        raise Exception        
        