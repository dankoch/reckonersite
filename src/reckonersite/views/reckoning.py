'''
Created on Aug 23, 2011
@author: danko
'''
import logging
import simplejson
import sys
import traceback
import uuid
import StringIO

from urllib import unquote_plus

from django import forms
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.cache import cache_page

from PIL import Image

from reckonersite.client.commentclient import client_post_reckoning_comment, \
                                              client_update_reckoning_comment, \
                                              client_delete_reckoning_comment
from reckonersite.client.mediaclient import client_post_reckoning_media, \
                                            client_get_reckoning_media, \
                                            client_delete_reckoning_media
from reckonersite.client.reckoningclient import client_get_reckoning, \
                                                client_post_reckoning, \
                                                client_update_reckoning, \
                                                client_get_related_open_reckonings, \
                                                client_get_related_closed_reckonings, \
                                                client_get_random_open_reckoning, \
                                                client_get_random_closed_reckoning, \
                                                client_get_reckonings, \
                                                client_reject_reckoning, \
                                                client_get_open_reckonings, \
                                                client_get_closed_reckonings
from reckonersite.client.voteclient import client_get_reckoning_answer_votes

from reckonersite.domain.ajaxserviceresponse import AjaxServiceResponse
from reckonersite.domain.answer import Answer
from reckonersite.domain.comment import Comment
from reckonersite.domain.media import Media, getDefaultThumbnailName, getDefaultFullName, getDefaultSmallName, \
                                             getDefaultUploadLocation, getDefaultUrl, parseReckoningImageFromUploadUrl
from reckonersite.domain.reckoning import Reckoning
from reckonersite.domain.reckoningajaxresponse import ReckoningAjaxResponse
from reckonersite.domain.vote import Vote
from reckonersite.views.vote import post_reckoning_vote, get_user_reckoning_vote
from reckonersite.util.dateutil import convertFormToDateTime
from reckonersite.util.math import computeReckoningAnswerPercentages
from reckonersite.util.validation import purgeHtml, sanitizeDescriptionHtml, sanitizeCommentHtml
from reckonersite.util.pagination import pageDisplay
from reckonersite.util.uploadhandler import ReckoningImageUploadHandler, FileTooBigException

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
                    
                    media = []
                    if (request.POST.get('attached-files', None)):
                        urls = request.POST.get('attached-files', None).split(";")
                        for url in urls:
                            media.append(parseReckoningImageFromUploadUrl(url))
    
                    reckoning=Reckoning(question=purgeHtml(form.cleaned_data['question']),
                                        description=sanitizeDescriptionHtml(form.cleaned_data['description']),
                                        answers=answers,
                                        tag_csv=purgeHtml(form.cleaned_data['tags']),
                                        submitter_id=request.user.reckoner_id,
                                        anonymous_requested=(form.cleaned_data['request_anonymous']),
                                        media_items=media)
                
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

    tags = forms.CharField(max_length=200, label="Tags", required=False)
    request_anonymous = forms.BooleanField(label="Post as Anonymous", initial=False, required=False)


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

###############################################################################################
# Displays the full contents of a standard Reckoning.
###############################################################################################

def get_reckoning(request, id = None, title = None):
    commentFormPrefix="commentform"
    redirect = False
        
    try:
        if request.method == 'GET':
            if (request.GET.get('redirect', "false") == "true"):
                redirect = True          
            
        if (redirect):
            service_response = client_get_reckoning(id, request.user.session_id)        
        else:
            service_response = client_get_reckoning(id, request.user.session_id, page_visit=True)
        
        # Check to see if the API submission was a success.  If not, straight to the fail-page!
        # If the Reckoning list is empty, there's no Reckoning by that ID.  Straight to the 404 page!
        # If the passed title doesn't match the slugified question matching the ID, redirect so that it does.
        if (not service_response.status.success):
            logger.warning("Error when retrieving reckoning: " + service_response.status.message)
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

            errors = request.session.get('errors', {})
            request.session['errors'] = None

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
    
###############################################################################################
# Displays the detailed results of a specific Reckoning.
###############################################################################################
    
def get_reckoning_results(request, id = None, title = None):
        
    try:         
        # Fetch the Reckoning. Don't count it as a view.   
        service_response = client_get_reckoning(id, request.user.session_id, page_visit=True)
        
        # Check to see if the API submission was a success.  If not, straight to the fail-page!
        # If the Reckoning list is empty, there's no Reckoning by that ID.  Straight to the 404 page!
        # If the passed title doesn't match the slugified question matching the ID, redirect so that it does.
        if (not service_response.status.success):
            logger.warning("Error when retrieving reckoning results: " + service_response.status.message)
            raise BaseException() 
        elif (not service_response.reckonings):
            raise Http404
        elif (request.path != service_response.reckonings[0].results_url):
            return HttpResponseRedirect(service_response.reckonings[0].results_url)
        else:        
            reckoning = computeReckoningAnswerPercentages(service_response.reckonings[0])
            vote_lists = []
            vote_counts = []
            for answer in reckoning.answers:
                vote_service_response = client_get_reckoning_answer_votes(id, answer.index, page=0, size=100, session_id = request.user.session_id)
                vote_lists.append(vote_service_response.votes)
                
                # Counts reflect number of votes besides what's in the vote lists
                vote_counts.append(int(vote_service_response.count) - len(vote_service_response.votes))
            
            # Pull the user's vote for this reckoning and add it to the context.
            user_vote = get_user_reckoning_vote(request, id=id)

            errors = request.session.get('errors', {})
            request.session['errors'] = None

            c = RequestContext(request, {'reckoning' : reckoning,
                                         'vote_lists' : vote_lists,
                                         'vote_counts' : vote_counts,
                                         'errors' : errors})
            
            return render_to_response('reckoning-results.html', c)
    except Http404:
        logger.debug("Received 404 looking for page: " + request.get_full_path())
        raise Http404
    except Exception:
        logger.error("Exception when showing reckoning results:") 
        logger.error(traceback.print_exc(8))
        raise Exception     

###############################################################################################
# The page responsible for processing a POST of a page comment.
#
# Receives:
#    The ID of the Reckoning to post the comment to
#    The Posted comment form
#    The URL to redirect to once finished.
###############################################################################################

def post_reckoning_comment(request):
    commentFormPrefix="commentform"
    redirect = "/"
    errors={}
    
    try:
        # Check to see if we're coming here from a POST.  If so, we've got work to do.
        if request.method == 'POST':
            redirect = request.POST.get('redirect', '/')   
            id = request.POST.get('reckoning-id', '/')   
            
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
                        logger.info("Invalid comment submitted: " + unicode(attr) + ": " + unicode(value))
                        errors[attr] = value
                            
        request.session['errors'] = errors 
        return HttpResponseRedirect(redirect)               
         
    except Exception:
        logger.error("Exception when showing a reckoning:") 
        logger.error(traceback.print_exc(8))
        raise Exception        
   
class CommentReckoningForm(forms.Form):
    comment = forms.CharField(max_length=5000, label="Comment", required=True, widget=forms.Textarea)  
    
###############################################################################################
# The page responsible for processing a POST of a reckoning vote.
#
# Receives:
#    The ID of the Reckoning to post the vote to
#    The posted vote
#    The URL to redirect to once finished.
###############################################################################################

def vote_reckoning(request):
    redirect = "/"
    errors={}
    
    #try:
        # Check to see if we're coming here from a POST.  If so, we've got work to do.
    if request.method == 'POST':
        redirect = request.POST.get('redirect', '/')
        
        if 'postvote' in request.POST:
            if (request.user.has_perm('VOTE')):
                if ('answer' in request.POST):
                    errors.update(post_reckoning_vote(request))
                        
    request.session['errors'] = errors   
    return HttpResponseRedirect(redirect)              
         
    #except Exception:
    #    logger.error("Exception when voting for a reckoning:") 
    #    logger.error(traceback.print_exc(8))
    #    raise Exception       
    
###############################################################################################
# The page responsible for showing a list of current open reckonings
###############################################################################################


def get_open_reckonings(request):

    page_url = "/open-reckonings"

    try:        
        # Check to see if we're coming here from a GET.  If so, we've got work to do.
        if request.method == 'GET':
            
            # Pull the relevant variables from the request string.
            include_tags = request.GET.get('include_tags', None)
            exclude_tags = request.GET.get('exclude_tags', None)
            page = request.GET.get('page', "1")
            size = request.GET.get('size', None)
            tab = request.GET.get('tab', None)
            
            # Persist the specified variables in the session for when the user navigates away and back.
            # Otherwise, pull the information out of the session
            if (include_tags is not None):
                request.session['open-include-tags'] = include_tags
            else:
                include_tags = request.session.get('open-include-tags', None)
    
            if (exclude_tags is not None): 
                request.session['open-exclude-tags'] = exclude_tags
            else:
                exclude_tags = request.session.get('open-exclude-tags', None)
                
            if (size):
                request.session['open-size'] = size
            else:
                size = request.session.get('open-size', '15')         
                
            if (tab):
                request.session['open-tab'] = tab
            else:
                tab = request.session.get('open-tab', 'newest')                         

            # Execute the correct action based on the selected tab and info.  Valid tabs:
            #  * 'popular', 'lastcall', 'featured', 'newest' (default)
            if (tab == "popular"):
                reckoning_response = client_get_open_reckonings(sort_by="views",
                                                                include_tags=include_tags, exclude_tags=exclude_tags,
                                                                page=(int(page)-1), size=size, 
                                                                session_id=request.user.session_id)
                        
            elif (tab == "lastcall"):
                reckoning_response = client_get_open_reckonings(sort_by="closingDate", ascending=True,
                                                                include_tags=include_tags, exclude_tags=exclude_tags,
                                                                page=(int(page)-1), size=size, 
                                                                session_id=request.user.session_id)
                
            elif (tab == "highlighted"):
                reckoning_response = client_get_open_reckonings(highlighted=True,
                                                                include_tags=include_tags, exclude_tags=exclude_tags,                                                                
                                                                page=(int(page)-1), size=size, 
                                                                session_id=request.user.session_id)
            else:
                tab = 'newest'
                reckoning_response = client_get_open_reckonings(page=(int(page)-1), size=size, 
                                                                include_tags=include_tags, exclude_tags=exclude_tags,                                                                
                                                                session_id=request.user.session_id)
            
            if not reckoning_response.status.success:
                logger.error("Open Reckoning Call failed: " + reckoning_response.status.message)
            
            context = {'reckonings' : reckoning_response.reckonings,
                                         'page' : int(page),
                                         'size' : int(size),
                                         'tab' : tab,
                                         'include_tags' : include_tags,
                                         'exclude_tags' : exclude_tags,
                                         'page_url' : page_url}
            
            context.update(pageDisplay(page, size, reckoning_response.count))
            c = RequestContext(request, context)
            
            return render_to_response('open_reckonings.html', c)
    except Exception:
        logger.error("Exception when showing the Open Reckonings list:") 
        logger.error(traceback.print_exc(8))
        raise Exception         
    
    
###############################################################################################
# The page responsible for showing a list of current closed reckonings
###############################################################################################


def get_closed_reckonings(request):

    page_url = "/finished-reckonings"

    try:        
        # Check to see if we're coming here from a GET.  If so, we've got work to do.
        if request.method == 'GET':
            
            # Pull the relevant variables from the request string.
            include_tags = request.GET.get('include_tags', None)
            exclude_tags = request.GET.get('exclude_tags', None)
            page = request.GET.get('page', "1")
            size = request.GET.get('size', None)
            tab = request.GET.get('tab', None)
            
            # Persist the specified variables in the session for when the user navigates away and back.
            # Otherwise, pull the information out of the session
            if (include_tags is not None):
                request.session['closed-include-tags'] = include_tags
            else:
                include_tags = request.session.get('closed-include-tags', None)
    
            if (exclude_tags is not None): 
                request.session['closed-exclude-tags'] = exclude_tags
            else:
                exclude_tags = request.session.get('closed-exclude-tags', None)
                
            if (size):
                request.session['closed-size'] = size
            else:
                size = request.session.get('closed-size', '15')         
                
            if (tab):
                request.session['closed-tab'] = tab
            else:
                tab = request.session.get('closed-tab', 'newest')                         

            # Execute the correct action based on the selected tab and info.  Valid tabs:
            #  * 'popular', 'leastpopular', 'featured', 'newest' (default)
            if (tab == "popular"):
                reckoning_response = client_get_closed_reckonings(sort_by="views",
                                                                include_tags=include_tags, exclude_tags=exclude_tags,
                                                                page=(int(page)-1), size=size, 
                                                                session_id=request.user.session_id)
                        
            elif (tab == "leastpopular"):
                reckoning_response = client_get_closed_reckonings(sort_by="views", ascending=True,
                                                                include_tags=include_tags, exclude_tags=exclude_tags,
                                                                page=(int(page)-1), size=size, 
                                                                session_id=request.user.session_id)
                
            elif (tab == "highlighted"):
                reckoning_response = client_get_closed_reckonings(sort_by="closingDate",
                                                                highlighted=True,
                                                                include_tags=include_tags, exclude_tags=exclude_tags,                                                                
                                                                page=(int(page)-1), size=size, 
                                                                session_id=request.user.session_id)
            else:
                tab = 'newest'
                reckoning_response = client_get_closed_reckonings(sort_by="closingDate",
                                                                page=(int(page)-1), size=size, 
                                                                include_tags=include_tags, exclude_tags=exclude_tags,                                                                
                                                                session_id=request.user.session_id)
            
            if not reckoning_response.status.success:
                logger.error("Closed Reckoning Call failed: " + reckoning_response.status.message)

            
            context = {'reckonings' : reckoning_response.reckonings,
                                         'page' : int(page),
                                         'size' : int(size),
                                         'tab' : tab,
                                         'include_tags' : include_tags,
                                         'exclude_tags' : exclude_tags,
                                         'page_url' : page_url}
            
            context.update(pageDisplay(page, size, reckoning_response.count))
            c = RequestContext(request, context)
            
            return render_to_response('closed_reckonings.html', c)
    except Exception:
        logger.error("Exception when showing the Closed Reckonings list:") 
        logger.error(traceback.print_exc(8))
        raise Exception   
    

###############################################################################################
# The page responsible for showing all Reckonings associated with a tab.
###############################################################################################


def get_tagged_reckonings(request, tag = None):
         
    try:
        page_url = "/reckonings/tag/" + tag
        tag = unquote_plus(tag)
        
        page = request.GET.get('page', "1")
        size = request.GET.get('size', None)
        tab = request.GET.get('tab', None)
        
        if (size):
            request.session['tag-size'] = size
        else:
            size = request.session.get('tag-size', '15')         
            
        if (tab):
            request.session['tag-tab'] = tab
        else:
            tab = request.session.get('tag-tab', 'newest')     
        
        if (tag):
            if (tab == "popular"):
                reckoning_response = client_get_reckonings(sort_by="views",
                                                                include_tags=tag,
                                                                page=(int(page)-1), size=size, 
                                                                session_id=request.user.session_id)
            elif (tab == "highlighted"):
                reckoning_response = client_get_reckonings(sort_by="closingDate",
                                                                highlighted=True,
                                                                include_tags=tag,                                                               
                                                                page=(int(page)-1), size=size, 
                                                                session_id=request.user.session_id)
            elif (tab == "closed"):
                reckoning_response = client_get_closed_reckonings(sort_by="closingDate",
                                                                include_tags=tag,
                                                                page=(int(page)-1), size=size, 
                                                                session_id=request.user.session_id)
            else:
                tab = 'open'
                reckoning_response = client_get_open_reckonings(sort_by="closingDate",
                                                                include_tags=tag,
                                                                page=(int(page)-1), size=size, 
                                                                session_id=request.user.session_id)
                
            if not reckoning_response.status.success:
                logger.error("Error when retrieving a tagged reckonings: " + reckoning_response.status.message)
                raise Exception 
           
            context = {'reckonings' : reckoning_response.reckonings,
                                         'page' : int(page),
                                         'size' : int(size),
                                         'include_tags' : tag,
                                         'tab' : tab,
                                         'page_url' : page_url}
            
            context.update(pageDisplay(page, size, reckoning_response.count))
            c = RequestContext(request, context)
        
            return render_to_response('tagged_reckonings.html', c)
                        
    except Exception:
        logger.error("Exception when showing tagged reckonings:") 
        logger.error(traceback.print_exc(8))
        raise Exception    
    
    
###############################################################################################
# The page responsible for getting a random reckoning.
###############################################################################################


def get_random_reckoning(request):     
    try:
        service_response = client_get_random_open_reckoning(request.user.session_id)
        
        if (service_response.status.success):
            return HttpResponseRedirect(service_response.reckonings[0].url)
        else:
            logger.error("Error when retrieving a random reckoning: " + service_response.status.message)
            raise Exception 
                        
    except Exception:
        logger.error("Exception when showing a reckoning:") 
        logger.error(traceback.print_exc(8))
        raise Exception    
    
   
###############################################################################################
# The endpoint responsible for getting the 'Top Reckonings' as used for the Top Reckonings widget
# (used for AJAX calls)
###############################################################################################

@cache_page(60 * 15)
def get_top_reckonings(request):     
    site_response = AjaxServiceResponse(success=False,
                                        message="whoops", 
                                        message_description='No go. Try again later.')
    
    if (request.user.has_perm('VIEW_RECKONING')):
        try:
            if (request.method == 'GET'):
                type = request.GET.get('type', 'open')
                
                if (type == 'closed'):
                    service_response = client_get_closed_reckonings(highlighted=True,
                                                                    randomize=True,
                                                                    size=4,
                                                                    session_id=request.user.session_id)
                else:
                    service_response = client_get_open_reckonings(highlighted=True,
                                                                    sort_by="closingDate",
                                                                    ascending=True,
                                                                    size=4,
                                                                    session_id=request.user.session_id)
                    
                if (service_response.status.success):
                    site_response = ReckoningAjaxResponse(reckonings=service_response.reckonings,
                                                          success=service_response.status.success)
                else:
                    logger.error("Error when retrieving top reckonings: " + service_response.status.message)
                            
        except Exception:
            logger.error("Exception when getting top reckonings:") 
            logger.error(traceback.print_exc(8))
            raise Exception    
    
    return HttpResponse(site_response.getXMLString())


###############################################################################################
# The endpoint responsible for getting related reckonings as used for the related reckonings widget
# (used for AJAX calls)
###############################################################################################

@cache_page(60 * 15)
def get_related_reckonings(request, id = None):     
    site_response = AjaxServiceResponse(success=False,
                                        message="whoops", 
                                        message_description='No go. Try again later.')
    
    if (request.user.has_perm('VIEW_RECKONING')):
        try:
            if (request.method == 'GET' and id):
                type = request.GET.get('type', 'open')
                
                if (type == 'closed'):
                    service_response = client_get_related_closed_reckonings(reckoning_id=id, 
                                                                            size=4, 
                                                                            session_id=request.user.session_id)
                else:
                    service_response = client_get_related_open_reckonings(reckoning_id=id, 
                                                                          size=4, 
                                                                          session_id=request.user.session_id)
                                        
                if (service_response.status.success):
                    site_response = ReckoningAjaxResponse(reckonings=service_response.reckonings,
                                                          success=service_response.status.success)
                else:
                    logger.error("Error when retrieving related reckonings: " + service_response.status.message)
                            
        except Exception:
            logger.error("Exception when getting related reckonings:") 
            logger.error(traceback.print_exc(8))
            raise Exception    
    
    return HttpResponse(site_response.getXMLString())
    
###############################################################################################
#  The endpoint responsible for deleting a reckoning comment.
#  (as used primarily for AJAX calls)
###############################################################################################

def delete_reckoning_comment(request):
    site_response = AjaxServiceResponse(success=False,
                                        message="whoops", 
                                        message_description='No go. Try again later.')
    
    if (request.user.has_perm('UPDATE_ALL_COMMENTS')):
        try:
            if request.method == 'POST':
                commentId = request.POST.get("comment-id", None)
                
                if (commentId):
                    service_response = client_delete_reckoning_comment(commentId, request.user.session_id)                          
                    
                    if (service_response.success):
                        site_response = AjaxServiceResponse(success=True,
                                                            message="success",
                                                            message_description="Deleted!")
                
        except Exception:
            logger.error("Exception when deleting a reckoning comment:") 
            logger.error(traceback.print_exc(8))    

    
    return HttpResponse(site_response.getXMLString())


###############################################################################################
#  The endpoint responsible for deleting a reckoning comment.
#  (as used primarily for AJAX calls)
###############################################################################################

def update_reckoning_comment(request, id = None):
    site_response = AjaxServiceResponse(success=False,
                                        message="whoops", 
                                        message_description='No go. Try again later.')
    
    if (request.user.has_perm('UPDATE_ALL_COMMENTS')):
        try:
            if request.method == 'POST':
                comment = sanitizeCommentHtml(request.POST.get("comment", ""))
                comment_id = request.POST.get("comment-id", None)
                
                if (len(comment) > 5000):
                    site_response = AjaxServiceResponse(success=False,
                                                        message="too_long",
                                                        message_description="Maximum Length is 5000 Characters (minus markup)")  
                elif (comment_id): 
                    commentUpdate = Comment(comment_id=comment_id, comment=comment)
                    service_response = client_update_reckoning_comment(commentUpdate,
                                                          request.user.session_id)                    
                    
                    if (service_response.success):
                        site_response = AjaxServiceResponse(success=True,
                                                            message="success",
                                                            message_description="Updated!")
                
        except Exception:
            logger.error("Exception when updating a reckoning comment:") 
            logger.error(traceback.print_exc(8))    

    
    return HttpResponse(site_response.getXMLString())

###############################################################################################
#  The endpoint responsible for updating a reckoning
#  (as used primarily for AJAX calls)
###############################################################################################

def update_reckoning_ajax(request):
    site_response = AjaxServiceResponse(success=False,
                                        message="whoops", 
                                        message_description='No go. Try again later.')
    
    if (request.user.has_perm('UPDATE_ALL_RECKONINGS')):
        try:
            if request.method == 'POST':
                reckoning_id = (request.POST.get('reckoning-id', None))
                
                commentary = sanitizeDescriptionHtml(request.POST.get('commentary', None))
                if (commentary):
                    commentary_user_id = request.user.reckoner_id
                else:
                    commentary_user_id = None                  
                
                question = purgeHtml(request.POST.get('question', None))
                description = sanitizeDescriptionHtml(request.POST.get('description', None))
                tag_csv = purgeHtml(request.POST.get('tags', None))
                closing_date = convertFormToDateTime(request.POST.get('time', None))
                
                if (request.POST.get('highlighted', None) is not None):
                    highlighted = (request.POST.get('highlighted', "false") == "true")
                else:
                    highlighted = None
                
                if ((commentary and len(commentary) > 3000) or (question and len(question) > 150) or 
                    (description and len(description) > 5000) or (tag_csv and len(tag_csv) > 200)):
                    site_response = AjaxServiceResponse(success=False,
                                                        message="too_long",
                                                        message_description="Saved field is too long.")  
                    
                elif (reckoning_id): 
                    reckoningUpdate = Reckoning(id=reckoning_id, commentary=commentary, commentary_user_id=commentary_user_id,
                                                question=question, description=description, tag_csv=tag_csv, closing_date=closing_date,
                                                highlighted=highlighted)
                    
                    service_response = client_update_reckoning(reckoningUpdate,
                                                          request.user.session_id)                    
                    
                    if (service_response.success):
                        site_response = AjaxServiceResponse(success=True,
                                                            message="success",
                                                            message_description="Updated!")
                
        except Exception:
            logger.error("Exception when updating a reckoning:") 
            logger.error(traceback.print_exc(8))    

    
    return HttpResponse(site_response.getXMLString())

###############################################################################################
#  The endpoint responsible for adding/overriding a Reckoning commentary piece.
#  (as used primarily for AJAX calls)
###############################################################################################

def delete_reckoning_commentary(request):
    site_response = AjaxServiceResponse(success=False,
                                        message="whoops", 
                                        message_description='No go. Try again later.')
    
    if (request.user.has_perm('UPDATE_ALL_RECKONINGS')):
        try:
            if request.method == 'POST':
                reckoning_id = (request.POST.get('reckoning-id', None))
                 
                if (reckoning_id): 
                    reckoningUpdate = Reckoning(id=reckoning_id, commentary="", 
                                                commentary_user_id="")
                    
                    service_response = client_update_reckoning(reckoningUpdate,
                                                          request.user.session_id)                    
                    
                    if (service_response.success):
                        site_response = AjaxServiceResponse(success=True,
                                                            message="success",
                                                            message_description="Deleted!")
                
        except Exception:
            logger.error("Exception when deleting reckoning commentary:") 
            logger.error(traceback.print_exc(8))    

    
    return HttpResponse(site_response.getXMLString())

###############################################################################################
#  The endpoint used to reject an already posted Reckoning.
#  (as used primarily for AJAX calls)
###############################################################################################

def reject_reckoning_ajax(request):
    site_response = AjaxServiceResponse(success=False,
                                        message="whoops", 
                                        message_description='No go. Try again later.')
    
    if (request.user.has_perm('APPROVAL')):
        try:
            if request.method == 'POST':
                reckoning_id = (request.POST.get('reckoning-id', None))
                 
                if (reckoning_id): 
                    service_response = client_reject_reckoning(reckoning_id,
                                                          request.user.session_id)                    
                    
                    if (service_response.success):
                        site_response = AjaxServiceResponse(success=True,
                                                            message="success",
                                                            message_description="Deleted! You're looking at a ghost!")
                
        except Exception:
            logger.error("Exception when rejecting a reckoning:") 
            logger.error(traceback.print_exc(8))    

    
    return HttpResponse(site_response.getXMLString())

###############################################################################################
#  The endpoint used to upload image files associated with a Reckoning.
#  This needs to tie into the BlueImp AJAX File Handler, and thus returns a JSON object as follows:
#
#  NAME
#  SIZE
#  URL
#  THUMBNAIL_URL
#  DELETE_URL
#  DELETE_TYPE
###############################################################################################

def image_upload_ajax(request):
    delete_url = "/ajax/reckoning/image/delete"
    scaled_image_size = 575, 575
    small_image_size = 300, 575
    thumbnail_size = 70, 70  
    #request.upload_handlers.insert(0, ReckoningImageUploadHandler())
    result = []
          
    if request.method == 'POST':
        if (request.user.has_perm('POST_RECKONING')):
            try:
                if request.FILES == None:
                    return HttpResponseBadRequest('Must have files attached!')
             
                ####### Downloading file data. #######
                id = str(uuid.uuid4())
                image_file = request.FILES[u'files[]']
                file_name = str(image_file.name)
                file_size = image_file.size
                content_type = image_file.content_type
                
                ####### Save four copies of the image to S3, specifically: ####### 
                              
                # (1) Original, Full Size Copy               
                default_storage.save(getDefaultUploadLocation(getDefaultFullName(file_name), id), image_file)   
                
                # (2) Scaled Copy for Display Within A One-Image Reckoning (treated as 'authoritative')               
                scaled_image = Image.open(image_file)
                scaled_image.thumbnail(scaled_image_size, Image.ANTIALIAS)
                scaled_image_io = StringIO.StringIO()
                
                if (content_type == "image/jpeg"):
                    scaled_image.save(scaled_image_io, format='JPEG')
                elif (content_type == "image/gif"):
                    scaled_image.save(scaled_image_io, format='GIF')
                else:
                    scaled_image.save(scaled_image_io, format='PNG')
                scaled_image_file = InMemoryUploadedFile(scaled_image_io, None, 
                                                            file_name, content_type, scaled_image_io.len, None)
                
                default_storage.save(getDefaultUploadLocation(file_name, id), scaled_image_file)      

                # (3) Scaled Copy for Display Within A Two-Image Reckoning              
                scaled_image.thumbnail(small_image_size, Image.ANTIALIAS)
                small_image_io = StringIO.StringIO()
                
                if (content_type == "image/jpeg"):
                    scaled_image.save(small_image_io, format='JPEG')
                elif (content_type == "image/gif"):
                    scaled_image.save(small_image_io, format='GIF')
                else:
                    scaled_image.save(small_image_io, format='PNG')
                small_image_file = InMemoryUploadedFile(small_image_io, None, 
                                                            getDefaultSmallName(file_name), content_type, small_image_io.len, None)
                
                default_storage.save(getDefaultUploadLocation(getDefaultSmallName(file_name), id), small_image_file)      

                # (4) A Thumbnail               
                thumbnail_image_io = StringIO.StringIO()
                scaled_image.thumbnail(thumbnail_size, Image.ANTIALIAS)
                
                if (content_type == "image/jpeg"):
                    scaled_image.save(thumbnail_image_io, format='JPEG')
                elif (content_type == "image/gif"):
                    scaled_image.save(thumbnail_image_io, format='GIF')
                else:
                    scaled_image.save(thumbnail_image_io, format='PNG')
                thumbnail_image_file = InMemoryUploadedFile(thumbnail_image_io, None, 
                                                            getDefaultThumbnailName(file_name), content_type, thumbnail_image_io.len, None)
                
                default_storage.save(getDefaultUploadLocation(getDefaultThumbnailName(file_name), id), thumbnail_image_file)
                
                # Set the 'authoritative' URL for this image forever more.
                image_url = getDefaultUrl(file_name, id)    
                              
                # Generate JSON Response
                result = []
                result.append({"name": file_name, 
                               "size": file_size, 
                               "url": image_url, 
                               "thumbnail_url": image_url,
                               "delete_url": "/".join((delete_url,id)), 
                               "delete_type":"POST",})
                
                response_data = simplejson.dumps(result)
                return HttpResponse(response_data, mimetype='application/json')                                
                    
            except FileTooBigException:
                logger.info("The uploaded file was too large:") 
                result.append({"error":"1",})
            except IOError:
                logger.error("IO error when uploading an image:") 
                logger.error(traceback.print_exc(8))  
                result.append({"error":"2",})
            except Exception:
                logger.error("Exception when uploading an image:") 
                logger.error(traceback.print_exc(8))    
    
    # Generic error response
    if not result:
        result.append({"error":"99",})
    response_data = simplejson.dumps(result)
    
    return HttpResponse(response_data, mimetype='application/json')   


###############################################################################################
#  The endpoint used to download image files associated with a Reckoning.
#  This needs to tie into the BlueImp AJAX File Handler, and thus returns a JSON object as follows:
#
#  NAME
#  SIZE
#  URL
#  THUMBNAIL_URL
#  DELETE_URL
#  DELETE_TYPE
###############################################################################################

def image_download_ajax(request, id):
    delete_url = "/ajax/reckoning/image/delete"
    result = []
          
    if request.method == 'GET' and id:
        if (request.user.has_perm('VIEW_RECKONING')):
            try:
                service_response = client_get_reckoning(id, request.user.session_id)    
                
                if (not service_response.status.success):
                    result.append({"error": "4",})
                    logger.error("Error when retrieving Reckoning images: " + str(service_response.status.message)) 
                elif (not service_response.reckonings):
                    result.append({"error": "5",})
                    logger.error("Reckoning not found when retrieving images: " + str(service_response.status.message)) 
                else:       
                    for reckoning in service_response.reckonings:
                        for media in reckoning.media_items:
                    
                            # Generate JSON Response
                            result.append({"name": media.name, 
                                           "size": media.size, 
                                           "url": media.url, 
                                           "thumbnail_url": media.url,
                                           "delete_url": "/".join((delete_url, media.media_id)), 
                                           "delete_type":"POST",})
                
                    response_data = simplejson.dumps(result)
                    return HttpResponse(response_data, mimetype='application/json')                                
                    
            except Exception:
                logger.error("Exception when retrieving Reckoning images:") 
                logger.error(traceback.print_exc(8))    
    
    # Generic error response
    if not result:
        result.append({"error":"99",})
    response_data = simplejson.dumps(result)
    return HttpResponse(response_data, mimetype='application/json')     

###############################################################################################
#  The endpoint used to add an uploaded image to an existing Reckoning.
#
#  NAME
#  SIZE
#  URL
#  THUMBNAIL_URL
#  DELETE_URL
#  DELETE_TYPE
###############################################################################################

def image_add_ajax(request, id = None):
    result = []
    
    if request.method == 'POST' and id:
        try:
            if (request.user.has_perm('UPDATE_ALL_RECKONINGS')):
             
                media = None
                url = request.POST.get('new-image', None)
                if (url):
                    media = parseReckoningImageFromUploadUrl(url)              
             
                if (media):
                    service_response = client_post_reckoning_media(media, id, request.user.session_id) 
             
                    # Generate JSON Response
                    if (service_response.success):                    
                        result.append({"success": "true",
                                       "name": id})
                     
                        response_data = simplejson.dumps(result)
                        return HttpResponse(response_data, mimetype='application/json')  
                    else:
                        logger.error("Error when adding media to Reckoning: " + service_response.message_description)
                        result.append({"success": "false",
                                       "error":"99",
                                       "message":service_response.message_description})            
                    
        except IOError:
            logger.error("IO error when deleting an image:") 
            logger.error(traceback.print_exc(8))  
            result.append({"error":"2",})
        except Exception:
            logger.error("Exception when deleting an image:") 
            logger.error(traceback.print_exc(8))    
    
    # Generic error response
    if not result:
        result.append({"error":"99",})
    response_data = simplejson.dumps(result)
    return HttpResponse(response_data, mimetype='application/json')   

###############################################################################################
#  The endpoint used to delete uploaded images attached to a reckoning.
#
#  NAME
#  SIZE
#  URL
#  THUMBNAIL_URL
#  DELETE_URL
#  DELETE_TYPE
###############################################################################################

def image_delete_ajax(request, id = None):
    result = []
    
    if request.method == 'POST' and id:
        try:

            # Check to see if the ID is attached to the Reckoning.  If so, the user needs
            # tougher permissions to execute the delete, and we need to pry it off afterwards.
            media_response = client_get_reckoning_media(id, request.user.session_id)
        
            if (request.user.has_perm('UPDATE_ALL_RECKONINGS') or
                 (request.user.has_perm('POST_RECKONING') and not media_response.reckonings)):
             
                # Delete the content from S3.
                files = default_storage.listdir(getDefaultUploadLocation(id=id))

                if (files[1]):
                    for file in files[1]:
                        default_storage.delete(getDefaultUploadLocation(name=file, id=id))
             
                if (media_response.reckonings):
                    client_delete_reckoning_media(id, request.user.session_id) 
             
                # Generate JSON Response
                result = []
                result.append({"success": "true",
                               "name": id})
             
                response_data = simplejson.dumps(result)
                return HttpResponse(response_data, mimetype='application/json')              
                    
        except IOError:
            logger.error("IO error when deleting an image:") 
            logger.error(traceback.print_exc(8))  
            result.append({"error":"2",})
        except Exception:
            logger.error("Exception when deleting an image:") 
            logger.error(traceback.print_exc(8))    
    
    # Generic error response
    if not result:
        result.append({"error":"99",})
    response_data = simplejson.dumps(result)
    return HttpResponse(response_data, mimetype='application/json')    