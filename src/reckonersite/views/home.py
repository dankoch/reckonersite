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

from reckonersite.auth import reckonerauthbackend
from reckonersite.client.facebookclient import client_get_facebook_user_token

logger = logging.getLogger(settings.STANDARD_LOGGER)

def home_page(request):
    try:    
        c = RequestContext(request, {'facebook_app_id' : settings.FACEBOOK_APP_ID,
                                     'facebook_redirect_url' : settings.FACEBOOK_REDIRECT_URL})
        
        return render_to_response('index.html', c)
    except Exception:      
        logger.error("Exception when rending home page:") 
        logger.error(traceback.print_exc(8))
        raise Exception