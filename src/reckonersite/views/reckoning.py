'''
Created on Aug 23, 2011
@author: danko
'''
import sys

from django import forms
from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from reckonersite.client.utilities import client_error_mapper
from reckonersite.client.reckoningclient import client_get_reckoning, client_post_reckoning
from reckonersite.domain.reckoning import Reckoning
from reckonersite.domain.answer import Answer

def post_reckoning(request):
    
    # Check to see if we're coming here from a POST.  If so, process it.  If not, give 'em a fresh form.
    if request.method == 'POST' :
        try:
            form = PostReckoningForm(request.POST)
            
            # Check form validation -- kick the form back out with error messages if failed.
            if not form.is_valid():
                for attr, value in form.errors:
                    messages.error(request, value, extra_tags='validation')
            else:
                # Build a Reckoning off of the form content
                answer1 = Answer(index = 0, text=form.cleaned_data['answer1'], subtitle=form.cleaned_data['answer1sub'])
                answer2 = Answer(index = 0, text=form.cleaned_data['answer2'], subtitle=form.cleaned_data['answer2sub'])
                reckoning = Reckoning(question = form.cleaned_data['question'], description = form.cleaned_data['description'],
                                      answers = (answer1, answer2,))
                
                # Submit to the API
                response = client_post_reckoning(reckoning, "none")
                
                # Check to see if the API submission was a success.  If not, clean the error and display.  Otherwise, great!
                if not response.success:
                    messages.error(request, 
                                   client_error_mapper(response.message), 
                                   extra_tags='api-error')
                else:                    
                    return HttpResponseRedirect('/thanks-for-playing')
            # Something bad happened, big time.  Time for the fail whale page.
        except:
            print "Exception when posting a reckoning:", sys.exc_info()[0]
            raise BaseException()
    else :
        form = PostReckoningForm()
    
    c = RequestContext(request,{'form' : form,})
    return render_to_response('post-reckoning.html', c)


class PostReckoningForm(forms.Form):
    question = forms.CharField(label="Your reckoning question!")
    description = forms.CharField(label="Explain what this is all about!")
    answer1 = forms.CharField(label="Answer 1")
    answer1sub = forms.CharField(label="Subtitle")
    answer2 = forms.CharField(label="Answer 2")
    answer2sub = forms.CharField(label="Subtitle") 


def post_reckoning_thanks(request):
    
    return render_to_response('post-reckoning-thanks.html')


def get_reckoning(request, id = None):
    
    request.session['place'] = request.get_full_path()
    service_response = client_get_reckoning(id, "none")
    
    # Check to see if the API submission was a success.  If not, straight to the fail-page!
    # If the Reckoning list is empty, there's no Reckoning by that ID.  Straight to the 404 page!
    if (not service_response.status.success):
        raise BaseException() 
    elif (not service_response.reckonings):
        raise Http404
    else:
        c = RequestContext(request, {'facebook_app_id' : settings.FACEBOOK_APP_ID,
                                     'facebook_redirect_url' : settings.FACEBOOK_REDIRECT_URL,
                                     'reckoning' : service_response.reckonings[0]})
        return render_to_response('reckoning.html', c)
        