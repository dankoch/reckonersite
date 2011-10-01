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

from reckonersite.client.utilities import client_error_mapper
from reckonersite.client.reckoningclient import client_get_reckoning, client_post_reckoning
from reckonersite.domain.reckoning import Reckoning
from reckonersite.domain.answer import Answer

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
        else :
            form = PostReckoningForm()
        
        c = RequestContext(request,{'form' : form,})
        return render_to_response('post-reckoning.html', c)
    except Exception:      
        logger.error("Exception when showing and processing the Submit-a-Reckoning form:") 
        logger.error(traceback.print_exc(8))
        raise Exception


class PostReckoningForm(forms.Form):
    question = forms.CharField(label="Your reckoning question!")
    description = forms.CharField(label="Explain what this is all about!")
    answer1 = forms.CharField(label="Answer 1")
    answer1sub = forms.CharField(label="Subtitle")
    answer2 = forms.CharField(label="Answer 2")
    answer2sub = forms.CharField(label="Subtitle") 



###############################################################################################
# The page responsible for thanking users who have posted a Reckoning.
###############################################################################################


def post_reckoning_thanks(request):
    
    return render_to_response('post-reckoning-thanks.html')


def get_reckoning(request, id = None):
    try:
        request.session['place'] = request.get_full_path()
        service_response = client_get_reckoning(id, "none")
        
        # Check to see if the API submission was a success.  If not, straight to the fail-page!
        # If the Reckoning list is empty, there's no Reckoning by that ID.  Straight to the 404 page!
        if (not service_response.status.success):
            raise BaseException() 
        elif (not service_response.reckonings):
            raise Http404
        else:
            c = RequestContext(request, {'reckoning' : service_response.reckonings[0]})
            return render_to_response('reckoning.html', c)
    except Http404:
        logger.debug("Received 404 looking for page: " + request.get_full_path())
        raise Http404
    except Exception:
        logger.error("Exception when showing a reckoning:") 
        logger.error(traceback.print_exc(8))
        raise Exception        
        