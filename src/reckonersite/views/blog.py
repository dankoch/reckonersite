'''
Created on Aug 23, 2011
@author: danko
'''
import logging
import sys
import traceback

from urllib import unquote_plus

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

from reckonersite.client.contentclient import client_get_contents

from reckonersite.domain.ajaxserviceresponse import AjaxServiceResponse
from reckonersite.domain.contentajaxresponse import ContentAjaxResponse
from reckonersite.domain.comment import Comment
from reckonersite.domain.content import Content
from reckonersite.util.dateutil import convertFormToDateTime
from reckonersite.util.validation import purgeHtml, sanitizeCommentHtml, sanitizeDescriptionHtml
from reckonersite.util.pagination import pageDisplay

from reckonersite.views.content import getContentTagContext, getContentMonthContext

logger = logging.getLogger(settings.STANDARD_LOGGER)


###############################################################################################
# Page responsible for listing blog content.  With no arguments, this is the blog main page.
###############################################################################################

def blog_list_page(request):
    page_url = "/blog"
    errors={}
    
    try:    
        if request.method == 'GET':
            page = request.GET.get('page', '1')
            size = request.GET.get('size', '5')
            tag = request.GET.get('tag', None)
            month = request.GET.get('month', None)
            year = request.GET.get('year', None)
            
            posted_after = None
            posted_before = None
            
            if (month and year):
                next_month = str(int(month) + 1)
                posted_after = convertFormToDateTime("".join((month,"/01/",year," 00:01")))
                posted_before = convertFormToDateTime("".join((next_month,"/01/",year," 00:01")))
                
            # Persist the filter information.  Keep it if we're moving across pages.
            if (tag is not None):
                request.session['blog-include-tags'] = tag
            elif (page):
                tag = request.session.get('blog-include-tags', None)
                
            if (posted_after is not None):
                request.session['blog-posted-after'] = posted_after
            elif (page):
                posted_after = request.session.get('blog-posted-after', None)
            if (posted_before is not None):
                request.session['blog-posted-before'] = posted_before
            elif (page):
                posted_before = request.session.get('blog-posted-before', None)
                
            content_list_response = client_get_contents(page=(int(page)-1), size=int(size), 
                                                        include_tags = tag,
                                                        posted_before=posted_before, posted_after=posted_after,
                                                        sort_by="postingDate", ascending=False)
            
            context = {'page': int(page),
                       'size': int(size),
                       'contents' : content_list_response.contents,
                       'page_url' : page_url,
                       'errors' : errors}
            context.update(pageDisplay(page, size, content_list_response.count))
            context.update(getContentTagContext(request))
            context.update(getContentMonthContext(request))
            
            c = RequestContext(request, context)
            
            return render_to_response('blog_list.html', c)
            
    except Exception:      
        logger.error("Exception when rending blog list page:") 
        logger.error(traceback.print_exc(8))
        raise Exception
    
    
###############################################################################################
#  The endpoint for retrieving the most recent blog posts for the sidebar
#  (as used primarily for AJAX calls)
###############################################################################################

def get_recent_blog_ajax(request, id = None):
    site_response = AjaxServiceResponse(success=False,
                                        message="whoops", 
                                        message_description='No go. Try again later.')
    
    if (request.user.has_perm('VIEW_CONTENT')):
        try:
            if request.method == 'GET':          
                size = request.GET.get("size", "1")
                
                service_response = client_get_contents(content_type="BLOG", page=0, size=int(size),
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