'''
Created on Aug 31, 2011

@author: danko
'''
import logging
import smtplib
import sys
import traceback

from django import forms
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from reckonersite.util.validation import purgeHtml
from reckonersite.util import captcha

logger = logging.getLogger(settings.STANDARD_LOGGER)    
    
def search_page(request):
    return render_to_response('search.html', RequestContext(request, None))

def about_page(request):
    return render_to_response('about.html', RequestContext(request, None))

def contact_us_page(request):
        
    try:
        if request.method == 'GET':
            contactUsForm = ContactUsForm()    

            errors = request.session.get('errors', {})
            request.session['errors'] = None

            c = RequestContext(request, {'form' : contactUsForm,
                                         'captcha_pub_key' : settings.CAPTCHA_PUBLIC_KEY,
                                         'errors' : errors})
            
            return render_to_response('contact-us.html', RequestContext(request, c))
    except Exception:
        logger.error("Exception when showing contact us page:") 
        logger.error(traceback.print_exc(8))
        raise Exception  
    
def submit_contact_us_page(request):   
    errors = {}

    try:
        if request.method == 'POST':
            if (request.user.has_perm('CONTACT_US')):
                captcha_response = captcha.submit(request.POST.get('recaptcha_challenge_field', ''), 
                                                  request.POST.get('recaptcha_response_field', ''), 
                                                  settings.CAPTCHA_PRIVATE_KEY, 
                                                  request.META.get('REMOTE_ADDR', ''))
                                                  
            if not captcha_response.is_valid:
                errors['contact_us_captcha']="Invalid captcha text.  Try again!"
            else:
                contactUsForm = ContactUsForm(request.POST)
                
                if (contactUsForm.is_valid()):
                    name = purgeHtml(contactUsForm.cleaned_data.get('name'))
                    email = purgeHtml(contactUsForm.cleaned_data.get('email'))
                    subject = purgeHtml(contactUsForm.cleaned_data.get('subject'))
                    message = purgeHtml(contactUsForm.cleaned_data.get('message'))
                    
                    email = EmailMessage(subject, "\n".join((name, email, message)), settings.CONTACT_US_EMAIL, 
                                         [settings.CONTACT_US_EMAIL], [],
                                         headers= {'Reply-To': email})
                    
                    email.send(False)
                    return HttpResponseRedirect('/contact-us-success')
                else:
                    for attr, value in contactUsForm.errors.iteritems():
                        logger.info("Invalid contact-us form submitted: " + unicode(attr) + ": " + unicode(value))
                        errors[attr] = value                

    except smtplib.SMTPException:
        logger.error("Mail sending exception when submitting contact us page:") 
        logger.error(traceback.print_exc(8))
        messages.error("Sorry!  Reckonbot is having trouble with the Contact Us form.  I'm on it! - DK")               
    except Exception:
        logger.error("Exception when submitting contact us page:") 
        logger.error(traceback.print_exc(8))
        raise Exception 

    request.session['errors'] = errors    
    return HttpResponseRedirect('/contact-us')                

class ContactUsForm(forms.Form):  
    name = forms.CharField(max_length=50, label="Name", required=True, widget=forms.Textarea)
    email = forms.CharField(max_length=200, label="Email", required=True, widget=forms.Textarea)
    subject = forms.CharField(max_length=200, label="Subject", required=True, widget=forms.Textarea)
    message = forms.CharField(max_length=3000, label="Subject", required=True, widget=forms.Textarea)

def contact_us_success_page(request):
    return render_to_response('contact-us-success.html', RequestContext(request, None))

def privacy_policy_page(request):
    return render_to_response('privacy-policy.html', RequestContext(request, None))