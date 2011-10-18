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

from reckonersite.client.commentclient import client_post_reckoning_comment
from reckonersite.client.reckoningclient import client_get_reckoning, \
                                                client_post_reckoning, \
                                                client_get_random_open_reckoning, \
                                                client_get_random_closed_reckoning

from reckonersite.domain.answer import Answer
from reckonersite.domain.comment import Comment
from reckonersite.domain.reckoning import Reckoning
from reckonersite.domain.vote import Vote
from reckonersite.views.vote import post_reckoning_vote, get_user_reckoning_vote
from reckonersite.util.math import computeReckoningAnswerPercentages
from reckonersite.util.validation import purgeHtml, sanitizeDescriptionHtml, sanitizeCommentHtml

logger = logging.getLogger(settings.STANDARD_LOGGER)


###############################################################################################
# The page responsible for the actual submission of new Reckonings.
###############################################################################################


def post_reckoning(request):
    
    if request.user.has_perm('POST_RECKONING'):  
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
                                        description=sanitizeDescriptionHtml(form.cleaned_data['description']),
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
    else:
        return HttpResponseRedirect("/post-reckoning-welcome")      

class PostReckoningForm(forms.Form):  
    question = forms.CharField(max_length=150, label="Question", required=True, widget=forms.Textarea)
    description = forms.CharField(max_length=3000, label="Description", required=False, widget=forms.Textarea)
    
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
    commentFormPrefix="commentform"
    errors={}
    
    try:
        # Check to see if we're coming here from a POST.  If so, we've got work to do.
        if request.method == 'POST':
            if 'postcomment' in request.POST:
                if (request.user.has_perm('COMMENT')):
                    commentForm = CommentReckoningForm(request.POST, prefix=commentFormPrefix)
                    if (commentForm.is_valid()):
                        comment = Comment(comment = sanitizeCommentHtml(commentForm.cleaned_data.get('comment')),
                                          poster_id = request.user.reckoner_id)
                        comment_service_response = client_post_reckoning_comment(comment, id, request.user.session_id)
                        if not comment_service_response.success:
                            logger.error("Failed to post comment to ID: " + id)
                            messages.error(request, "Sorry!  Reckonbot choked on that last comment!  I'm looking into it, ASAP.  - DK")
                    else:
                        for attr, value in commentForm.errors.iteritems():
                            logger.info("Invalid comment submitted: " + str(attr) + ": " + str(value))
                            errors[attr] = value
                            
                service_response = client_get_reckoning(id, request.user.session_id)
                                                  
            elif 'postvote' in request.POST:
                if (request.user.has_perm('VOTE')):
                    if ('answer' in request.POST):
                        errors.update(post_reckoning_vote(request))
        
                service_response = client_get_reckoning(id, request.user.session_id)        
        
        else:
            service_response = client_get_reckoning(id, request.user.session_id, page_visit=True)
        
        # Check to see if the API submission was a success.  If not, straight to the fail-page!
        # If the Reckoning list is empty, there's no Reckoning by that ID.  Straight to the 404 page!
        # If the passed title doesn't match the slugified question matching the ID, redirect so that it does.
        if (not service_response.status.success):
            raise BaseException() 
        elif (not service_response.reckonings):
            raise Http404
        elif (request.path != service_response.reckonings[0].url):
            return HttpResponseRedirect(service_response.reckonings[0].url)
        else:
            commentForm = CommentReckoningForm(prefix=commentFormPrefix)            
            reckoning = computeReckoningAnswerPercentages(service_response.reckonings[0])
            next_reck = None
            prev_reck = None
            
            # Pull the user's vote for this reckoning and add it to the context.
            user_vote = get_user_reckoning_vote(request, id=id)
            
            # Get the Next and Last Reckoning items for the display.  Get open reckonings if the current
            # reckoning is open, and vice versa.  
            if (reckoning.open):
                next_reck_response = client_get_random_open_reckoning(request.user.session_id)
                prev_reck_response = client_get_random_open_reckoning(request.user.session_id)
            else:
                next_reck_response = client_get_random_closed_reckoning(request.user.session_id)
                prev_reck_response = client_get_random_closed_reckoning(request.user.session_id)                
            
            if (next_reck_response.reckonings):
                next_reck = next_reck_response.reckonings[0]
            if (prev_reck_response.reckonings):
                prev_reck = prev_reck_response.reckonings[0]

            c = RequestContext(request, {'reckoning' : reckoning,
                                         'user_vote' : user_vote,
                                         'next_reck' : next_reck,
                                         'prev_reck' : prev_reck,
                                         'errors' : errors})
            
            return render_to_response('reckoning.html', c)
    except Http404:
        logger.debug("Received 404 looking for page: " + request.get_full_path())
        raise Http404
    except Exception:
        logger.error("Exception when showing a reckoning:") 
        logger.error(traceback.print_exc(8))
        raise Exception     
    
    
class CommentReckoningForm(forms.Form):  
    comment = forms.CharField(max_length=5000, label="Comment", required=True, widget=forms.Textarea)  
        