'''
Created on Aug 31, 2011

@author: danko
'''
import sys

from django import forms
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from reckonersite.client.facebookclient import client_get_facebook_user_token


def login(request):
    c = RequestContext(request, {'facebook_app_id' : settings.FACEBOOK_APP_ID,
                                 'facebook_redirect_url' : settings.FACEBOOK_REDIRECT_URL})
    
    return render_to_response('test_login.html', RequestContext(request, c))        


def login_facebook(request):
    
    if request.method == 'GET':
        code = request.GET.get('code')
        
        if (code):
            access_token = client_get_facebook_user_token(code)
            print "YY " + access_token.access_token
            
            if (access_token.access_token):
                return HttpResponseRedirect('/logged-in')
            else:
                raise BaseException() 
        else:
            if (request.GET.get('error') == 'access_denied'):
                return HttpResponseRedirect('/no-sweat')
            elif (request.GET.get('error')):
                raise BaseException()                          
    
    return login(request)  


def logged_in(request):
    lastUrl = request.session.get('place', None)
    
    if (lastUrl):
        return HttpResponseRedirect(lastUrl)
    else:
        return render_to_response('logged_in.html', RequestContext(request, None))


def rejected_login(request):
    return render_to_response('rejected_login.html', RequestContext(request, None))