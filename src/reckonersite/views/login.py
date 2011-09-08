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

def login_page(request):
    try:    
        c = RequestContext(request, {'facebook_app_id' : settings.FACEBOOK_APP_ID,
                                     'facebook_redirect_url' : settings.FACEBOOK_REDIRECT_URL})
        
        return render_to_response('test_login.html', RequestContext(request, c))
    except Exception:      
        logger.error("Exception when rending login screen:") 
        logger.error(traceback.print_exc(8))
        raise Exception

def login_facebook(request):
    '''
    View responsible for coordinating the server-side OAuth2 calls with Facebook.  Called upon
    redirect after the user has authenticated to Facebook and granted permissions to The Reckoner.
    
    Uses OAuth receipt (including user_token and expiration span) from Facebook and passes to 
    Reckoner Content Services to create a session.  Then applies this information to the session for
    the Reckoner Middleware to manage from this point onwards.
    '''
    try:
        if request.method == 'GET':
            code = request.GET.get('code')
            
            if (code):
                oAuthReceipt = client_get_facebook_user_token(code)
                user = reckonerauthbackend.authenticate(oAuthReceipt = oAuthReceipt)
                # If the user exists and is active, set the session user_token and expiration date
                # as provided from the Reckoning Content Services 
                if (user is not None):
                    if (user.active):
                        request.session[settings.RECKONER_TOKEN_ID] = user.user_token
                        request.session.set_expiry(user.expiration_date)                                        
                if (oAuthReceipt.user_token):
                    return HttpResponseRedirect('/login/howdy')
                else:
                    raise BaseException() 
            else:
                if (request.GET.get('error') == 'access_denied'):
                    return HttpResponseRedirect('/login/no-sweat')
                elif (request.GET.get('error')):
                    raise BaseException()                          
        
        return login_page(request)  
    except Exception:      
        logger.error("Exception when logging user in from Facebook:") 
        logger.error(traceback.print_exc(8))
        raise Exception

def logged_in(request):
    try:
        lastUrl = request.session.get(settings.LAST_SITE_TOKEN_ID, None)
        
        if (lastUrl):
            return HttpResponseRedirect(lastUrl)
        else:
            return render_to_response('logged_in.html', RequestContext(request, None))
    except Exception:      
        logger.error("Exception when rending logged-in screen:") 
        logger.error(traceback.print_exc(8))
        raise Exception

def rejected_login(request):
    return render_to_response('rejected_login.html', RequestContext(request, None))

def logout(request):
    reckonerauthbackend.logout_user(request.session.get(settings.RECKONER_TOKEN_ID, None))
    request.session.flush()
    if hasattr(request, '_cached_user'):
        del request._cached_user 
            
    return HttpResponseRedirect('/')