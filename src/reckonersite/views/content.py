'''
Created on Aug 23, 2011
@author: danko
'''
import datetime
import logging
import traceback

from django import forms
from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from reckonersite.client.commentclient import client_post_content_comment, \
                                              client_update_content_comment, \
                                              client_delete_content_comment

from reckonersite.client.contentclient import client_post_content, \
                                              client_get_content, \
                                              client_get_content_types, \
                                              client_update_content, \
                                              client_reject_content, \
                                              client_get_content_tags

from reckonersite.domain.ajaxserviceresponse import AjaxServiceResponse
from reckonersite.domain.comment import Comment
from reckonersite.domain.content import Content
from reckonersite.util.validation import purgeHtml, sanitizeCommentHtml, sanitizeDescriptionHtml

logger = logging.getLogger(settings.STANDARD_LOGGER)


###############################################################################################
# The page responsible for the actual submission of new content
###############################################################################################

def post_content(request):
    
    if request.user.has_perm('POST_CONTENT'):  
        try:
            # Check to see if we're coming here from a POST.  If so, process it.  If not, give 'em a fresh form.
            if request.method == 'POST' :
                form = PostContentForm(request.POST, content_types=client_get_content_types(request.user.session_id).data)
                
                # Check form validation -- kick the form back out with error messages if failed.
                if form.is_valid():
                    content=Content(content_type=(form.cleaned_data['content_type']),
                                        title=purgeHtml(form.cleaned_data['title']),
                                        body=(form.cleaned_data['body']),
                                        summary=(form.cleaned_data['summary']),
                                        tag_csv=purgeHtml(form.cleaned_data['tags']),
                                        submitter_id=request.user.reckoner_id)
                
                    # Submit to the API
                    response = client_post_content(content, request.user.session_id)
                    
                    # Check to see if the API submission was a success.  If not, clean the error and display.  Otherwise, great!
                    if not response.success:
                        logger.error("Error from post attempt: " + response.message)
                        raise Exception
                    else:                    
                        return HttpResponseRedirect('/blog')
            else:
                form = PostContentForm(content_types=client_get_content_types(request.user.session_id).data)
            
            c = RequestContext(request,{'form' : form,})
            return render_to_response('post-content.html', c)
        except Exception:      
            logger.error("Exception when showing and processing the Submit-Content form:") 
            logger.error(traceback.print_exc(8))
            raise Exception  
    else:
        return HttpResponseRedirect("/")      

class PostContentForm(forms.Form):  
    def __init__(self, *args, **kwargs):
        content_types = None
        if ("content_types" in kwargs):
            content_types = kwargs.pop("content_types")
            
        super(PostContentForm, self).__init__(*args, **kwargs)
        
        content_choices = []
        if (content_types):
            for content_type in content_types:
                content_choices.append((content_type, content_type))

        self.fields["content_type"] = forms.ChoiceField(label="Content Type", choices=content_choices, required=True)        
        self.fields["title"] = forms.CharField(max_length=300, label="Title", required=True, widget=forms.Textarea)
        self.fields["body"] = forms.CharField(max_length=50000, label="Body", required=True, widget=forms.Textarea)
        self.fields["summary"] = forms.CharField(max_length=500, label="Summary", required=False, widget=forms.Textarea)
        self.fields["tags"] = forms.CharField(max_length=200, label="Tags", required=False)
        

###############################################################################################
# The page responsible for retrieving a particular piece of content.
###############################################################################################

def get_content(request, id = None, title = None):
    page_url = "/content"
    commentFormPrefix="commentform"
    redirect = False
        
    try:
        if request.method == 'GET':
            if (request.GET.get('redirect', "false") == "true"):
                redirect = True          
            
        if (redirect):
            service_response = client_get_content(id, request.user.session_id)        
        else:
            service_response = client_get_content(id, request.user.session_id, page_visit=True)
        
        # Check to see if the API submission was a success.  If not, straight to the fail-page!
        # If the Content list is empty, there's no Content by that ID.  Straight to the 404 page!
        # If the passed title doesn't match the slugified question matching the ID, redirect so that it does.
        if (not service_response.status.success):
            logger.warning("Error when retrieving content: " + service_response.status.message)
            raise BaseException() 
        elif (not service_response.contents):
            raise Http404
        elif (request.path != service_response.contents[0].url):
            return HttpResponseRedirect(service_response.contents[0].url)
        else:
            commentForm = CommentReckoningForm(prefix=commentFormPrefix)            
            content = service_response.contents[0]
            errors = request.session.get('errors', {})
            request.session['errors'] = None
            
            context = {'content' : content,
                       'errors' : errors,
                       'page_url' : page_url  }
            context.update(getContentTagContext(request))
            context.update(getContentMonthContext(request))

            c = RequestContext(request, context)
            
            return render_to_response('content.html', c)
    except Http404:
        logger.debug("Received 404 looking for page: " + request.get_full_path())
        raise Http404
    except Exception:
        logger.error("Exception when showing a reckoning:") 
        logger.error(traceback.print_exc(8))
        raise Exception     

###############################################################################################
# The page responsible for processing a POST of a page comment.
#
# Receives:
#    The ID of the Content to post the comment to
#    The Posted comment form
#    The URL to redirect to once finished.
###############################################################################################

def post_content_comment(request):
    commentFormPrefix="commentform"
    redirect = "/"
    errors={}
    
    try:
        # Check to see if we're coming here from a POST.  If so, we've got work to do.
        if request.method == 'POST':
            redirect = request.POST.get('redirect', '/')   
            id = request.POST.get('content-id', '/')   
            
            if (request.user.has_perm('COMMENT')):
                commentForm = CommentReckoningForm(request.POST, prefix=commentFormPrefix)
                if (commentForm.is_valid()):
                    comment = Comment(comment = sanitizeCommentHtml(commentForm.cleaned_data.get('comment')),
                                      poster_id = request.user.reckoner_id)
                    comment_service_response = client_post_content_comment(comment, id, request.user.session_id)
                    if not comment_service_response.success:
                        logger.error("Failed to post comment to ID: " + id)
                        messages.error(request, "Sorry!  Reckonbot choked on that last comment!  I'm looking into it, ASAP.  - DK")
                else:
                    for attr, value in commentForm.errors.iteritems():
                        logger.info("Invalid comment submitted: " + str(attr) + ": " + str(value))
                        errors[attr] = value
                            
        request.session['errors'] = errors 
        return HttpResponseRedirect(redirect)               
         
    except Exception:
        logger.error("Exception when posting content comment:") 
        logger.error(traceback.print_exc(8))
        raise Exception        
   
class CommentReckoningForm(forms.Form):
    comment = forms.CharField(max_length=5000, label="Comment", required=True, widget=forms.Textarea)
    
    
###############################################################################################
#  The endpoint responsible for deleting a content comment.
#  (as used primarily for AJAX calls)
###############################################################################################

def delete_content_comment(request):
    site_response = AjaxServiceResponse(success=False,
                                        message="whoops", 
                                        message_description='No go. Try again later.')
    
    if (request.user.has_perm('UPDATE_ALL_COMMENTS')):
        try:
            if request.method == 'POST':
                commentId = request.POST.get("comment-id", None)
                
                if (commentId):
                    service_response = client_delete_content_comment(commentId, request.user.session_id)                          
                    
                    if (service_response.success):
                        site_response = AjaxServiceResponse(success=True,
                                                            message="success",
                                                            message_description="Deleted!")
                
        except Exception:
            logger.error("Exception when deleting content comment:") 
            logger.error(traceback.print_exc(8))    

    
    return HttpResponse(site_response.getXMLString())


###############################################################################################
#  The endpoint responsible for deleting a content comment.
#  (as used primarily for AJAX calls)
###############################################################################################

def update_content_comment(request, id = None):
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
                    service_response = client_update_content_comment(commentUpdate,
                                                          request.user.session_id)                    
                    
                    if (service_response.success):
                        site_response = AjaxServiceResponse(success=True,
                                                            message="success",
                                                            message_description="Updated!")
                
        except Exception:
            logger.error("Exception when updating a content comment:") 
            logger.error(traceback.print_exc(8))    

    
    return HttpResponse(site_response.getXMLString())

###############################################################################################
#  The endpoint responsible for updating a piece of content
#  (as used primarily for AJAX calls)
###############################################################################################

def update_content_ajax(request):
    site_response = AjaxServiceResponse(success=False,
                                        message="whoops", 
                                        message_description='No go. Try again later.')
    
    if (request.user.has_perm('UPDATE_ALL_CONTENT')):
        try:
            if request.method == 'POST':
                content_id = (request.POST.get('content-id', None))
                
                commentary = sanitizeDescriptionHtml(request.POST.get('commentary', None))
                if (commentary):
                    commentary_user_id = request.user.reckoner_id
                else:
                    commentary_user_id = None                  
                
                title = purgeHtml(request.POST.get('title', None))
                body = request.POST.get('body', None)
                tag_csv = purgeHtml(request.POST.get('tags', None))
                
                if ((commentary and len(commentary) > 3000) or (title and len(title) > 300) or 
                    (body and len(body) > 50000) or (tag_csv and len(tag_csv) > 200)):
                    site_response = AjaxServiceResponse(success=False,
                                                        message="too_long",
                                                        message_description="Saved field is too long.")  
                    
                elif (content_id): 
                    contentUpdate = Content(id=content_id, commentary=commentary, commentary_user_id=commentary_user_id,
                                                title=title, body=body, tag_csv=tag_csv)
                    
                    service_response = client_update_content(contentUpdate,
                                                          request.user.session_id)                    
                    
                    if (service_response.success):
                        site_response = AjaxServiceResponse(success=True,
                                                            message="success",
                                                            message_description="Updated!")
                
        except Exception:
            logger.error("Exception when updating content:") 
            logger.error(traceback.print_exc(8))    

    
    return HttpResponse(site_response.getXMLString())

###############################################################################################
#  The endpoint responsible for adding/overriding a content commentary piece.
#  (as used primarily for AJAX calls)
###############################################################################################

def delete_content_commentary(request):
    site_response = AjaxServiceResponse(success=False,
                                        message="whoops", 
                                        message_description='No go. Try again later.')
    
    if (request.user.has_perm('UPDATE_ALL_CONTENT')):
        try:
            if request.method == 'POST':
                content_id = (request.POST.get('content-id', None))
                 
                if (content_id): 
                    contentUpdate = Content(id=content_id, commentary="", 
                                                commentary_user_id="")
                    
                    service_response = client_update_content(contentUpdate,
                                                          request.user.session_id)                    
                    
                    if (service_response.success):
                        site_response = AjaxServiceResponse(success=True,
                                                            message="success",
                                                            message_description="Deleted!")
                
        except Exception:
            logger.error("Exception when deleting content commentary:") 
            logger.error(traceback.print_exc(8))    

    
    return HttpResponse(site_response.getXMLString())

###############################################################################################
#  The endpoint used to reject an already posted piece of content.
#  (as used primarily for AJAX calls)
###############################################################################################

def reject_content_ajax(request):
    site_response = AjaxServiceResponse(success=False,
                                        message="whoops", 
                                        message_description='No go. Try again later.')
    
    if (request.user.has_perm('APPROVAL')):
        try:
            if request.method == 'POST':
                content_id = (request.POST.get('content-id', None))
                 
                if (content_id): 
                    service_response = client_reject_content(content_id,
                                                          request.user.session_id)                    
                    
                    if (service_response.success):
                        site_response = AjaxServiceResponse(success=True,
                                                            message="success",
                                                            message_description="Deleted! You're looking at a ghost!")
                
        except Exception:
            logger.error("Exception when rejecting content:") 
            logger.error(traceback.print_exc(8))    

    
    return HttpResponse(site_response.getXMLString())


###############################################################################################
#  Utility used to add tags to the request context for the blog sidebar
###############################################################################################

def getContentTagContext(request):
    '''
    Calls the service necessary to pull all of the tags used for content and prepares them
    for the display context.
    '''
    nav_tags=[]

    service_response = client_get_content_tags(request.user.session_id)
    if (service_response.status.success):
        nav_tags = service_response.tags

    return ({'nav_tags' : nav_tags})

###############################################################################################
#  Utility used to add the monthly breakdown to the blog sidebar.
###############################################################################################

def getContentMonthContext(request):
    '''
    Calls the service necessary to pull the month categories used for content and prepares them
    for the display context.
    '''
    content_months=[]
    
    current_time = datetime.datetime.now()
    current_month = current_time.month
    current_year = current_time.year

    start_month=10
    start_year=2011
    
    while (current_month != start_month or current_year != start_year):
        content_months.append(datetime.date(current_year, current_month, 1))
        
        current_month -= 1;
        if (current_month < 1):
            current_month = 12;
            current_year -= 1;
    
    return ({'content_months' : content_months})
