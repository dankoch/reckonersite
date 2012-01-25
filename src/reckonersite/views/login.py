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
from reckonersite.client.googleclient import client_get_google_user_token

logger = logging.getLogger(settings.STANDARD_LOGGER)

def login_page(request):
    try:    
        
        return render_to_response('test_login.html', RequestContext(request, {}))
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
                if (user is not None) and (user.session_id is not None):
                    if (user.active):
                        request.session[settings.RECKONER_API_SESSION_ID] = user.session_id
                        request.session.set_expiry(user.expiration_date) 
                        
                        if (user.is_new_user):
                            return HttpResponseRedirect('/login/new-user-welcome')
                        
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


def login_google(request):
    '''
    View responsible for coordinating the server-side OAuth2 calls with Google.  Called upon
    redirect after the user has authenticated to Google and granted permissions to The Reckoner.
    
    Uses OAuth receipt (including user_token and expiration span) from Google and passes to 
    Reckoner Content Services to create a session.  Then applies this information to the session for
    the Reckoner Middleware to manage from this point onwards.
    '''
    try:
        if request.method == 'GET':
            code = request.GET.get('code')
            
            if (code):
                oAuthReceipt = client_get_google_user_token(code)
                user = reckonerauthbackend.authenticate(oAuthReceipt = oAuthReceipt)
                
                # If the user exists and is active, set the session user_token and expiration date
                # as provided from the Reckoning Content Services 
                if (user is not None):
                    if (user.active):
                        request.session[settings.RECKONER_API_SESSION_ID] = user.session_id
                        
                        # Google sessions can be renewed, so don't set the expiry date.
                        # request.session.set_expiry(user.expiration_date)
                        if (user.is_new_user):
                            return HttpResponseRedirect('/login/new-user-welcome')
                        
                        return HttpResponseRedirect('/login/howdy')
                    if (user.is_invalid_google_user):
                        return HttpResponseRedirect('/login/tricky-ol-google')                                        
                else:
                    raise BaseException() 
            else:
                if (request.GET.get('error') == 'access_denied'):
                    return HttpResponseRedirect('/login/no-sweat')
                elif (request.GET.get('error')):
                    raise BaseException()                          
        
        return login_page(request)  
    except Exception:      
        logger.error("Exception when logging user in from Google:") 
        logger.error(traceback.print_exc(8))
        raise Exception


def logged_in(request):
    try:
        lastUrl = request.session.get(settings.LAST_SITE_TOKEN_ID, None)
        
        if (lastUrl):
            return HttpResponseRedirect(lastUrl)
        else:
            return HttpResponseRedirect("/")
    except Exception:      
        logger.error("Exception when rending logged-in screen:") 
        logger.error(traceback.print_exc(8))
        raise Exception

def sign_up_page(request):
    return render_to_response('how-to-sign-up.html', RequestContext(request, None))

def new_user_welcome(request):
    return render_to_response('new-user-welcome.html', RequestContext(request, None))

def rejected_login(request):
    return render_to_response('rejected_login.html', RequestContext(request, None))

def rejected_login_bad_google(request):
    '''
    View for cases where a user has attempted to log in with a Google account that isn't
    a G+ (or Buzz) enabled account.  Google Accounts need a profile to log in.
    '''
    return render_to_response('rejected_login_bad_google.html', RequestContext(request, None))

def logout(request):
    reckonerauthbackend.logout_user(request.session.get(settings.RECKONER_API_SESSION_ID, None))
    request.session.flush()
    if hasattr(request, '_cached_user'):
        del request._cached_user 
            
    return HttpResponseRedirect('/')