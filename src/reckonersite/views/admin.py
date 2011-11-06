'''
Created on Aug 31, 2011

@author: danko
'''
import logging
import sys
import traceback

from django import forms
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from reckonersite.auth import reckonerauthbackend
from reckonersite.client.reckoningclient import client_get_reckoning_approval_queue, \
                                                client_get_reckoning, \
                                                client_update_reckoning, \
                                                client_approve_reckoning, \
                                                client_reject_reckoning
from reckonersite.domain.answer import Answer
from reckonersite.domain.reckoning import Reckoning
from reckonersite.util.validation import purgeHtml, sanitizeDescriptionHtml

logger = logging.getLogger(settings.STANDARD_LOGGER)

###############################################################################################
# The page responsible for updating/removing user permissions.  
# Reserved for ADMINs w/ the 'CHANGE_PERMISSIONS' permission.
###############################################################################################

def admin_page(request):
    if request.user.has_group('ADMIN') or request.user.has_group('SUPER_ADMIN'):
        try:
            c = RequestContext(request, {})
            return render_to_response("admin_home.html", c)  
        except Exception:      
            logger.error("Exception when rending admin screen:") 
            logger.error(traceback.print_exc(8))
            raise Exception
    else:
        return HttpResponseRedirect('/')      

###############################################################################################
# The page responsible for updating/removing user permissions.  
# Reserved for ADMINs w/ the 'CHANGE_PERMISSIONS' permission.
###############################################################################################

def user_permissions_page(request):
    if request.user.has_perm('UPDATE_PERMS'):
        try:
            groupList = reckonerauthbackend.get_group_list()
            groupFormPrefix = "groupform"
            userFormPrefix = "userform"

            if request.method == 'POST' :
                if 'getuser' in request.POST:
                    getUserForm = GetUserForm(request.POST, prefix=userFormPrefix)
                    
                    if not getUserForm.is_valid() :
                        for attr, value in getUserForm.errors.iteritems():
                            messages.error(request, value, extra_tags='validation')  
                    else:
                        userId = getUserForm.cleaned_data['userid']
                        currentUser = reckonerauthbackend.get_user(request.user.session_id, 
                                                                   userId)
                        
                        if not currentUser:
                            messages.error(request, "User not found.", extra_tags='user')  
                        else:
                            request.session['admin_edit_user'] = currentUser
                            
                elif 'setperms' in request.POST:
                    getUserForm = GetUserForm(prefix=userFormPrefix)
                    groupForm = SetUserGroup(request.POST, request.FILES, prefix=groupFormPrefix)
                    currentUser = request.session.get('admin_edit_user', None)  
                    groupMembership = []
                    active = True

                    if not groupForm.is_valid() :
                        for attr, value in groupForm.errors.iteritems():
                            messages.error(request, value, extra_tags='validation')  
                    else:
                        for group in groupList:
                            if ((groupFormPrefix + '-' + group) in groupForm.cleaned_data):
                                groupMembership.append(group)
                        if (len(groupMembership) == 0):
                            active = False
                            
                        reckonerauthbackend.change_user_permissions('REPLACE', groupMembership, 
                                                                    active, currentUser.reckoner_id, 
                                                                    request.user.session_id)

                        currentUser = reckonerauthbackend.get_user(request.user.session_id, 
                                                                   currentUser.reckoner_id)
                        request.session['admin_edit_user'] = currentUser    
                        
                        messages.success(request, 'User permissions changed.', extra_tags='success')

            getUserForm = GetUserForm(prefix=userFormPrefix)
            currentUser = request.session.get('admin_edit_user', None) 
            
            if (currentUser):                
                currentGroups = {}
                for group in groupList:
                    currentGroups[group] = (group in currentUser.groups)
                groupForm = SetUserGroup(prefix=groupFormPrefix, groups=currentGroups)
            else:
                groupForm=None 
            
            c = RequestContext(request, {'userForm': getUserForm, 
                                         'groupForm' : groupForm,
                                         'currentUser' : currentUser})
            
            return render_to_response('user_permissions_page.html', c)
        except Exception:      
            logger.error("Exception when rending user permission screen:") 
            logger.error(traceback.print_exc(8))
            raise Exception
    else:
        return HttpResponseRedirect('/')        


class GetUserForm(forms.Form):
    userid = forms.CharField(label="User ID to View: ")
    
class SetUserGroup(forms.Form):
    def __init__(self, groups, *args, **kwargs):
        super(SetUserGroup, self).__init__(*args, **kwargs)
        
        if (groups):
            for group, value in groups.iteritems():
                self.fields[group] = forms.BooleanField(initial = value, required=False)


###############################################################################################
# The page responsible for updating/removing user permissions.  
# Reserved for ADMINs w/ the 'CHANGE_PERMISSIONS' permission.
###############################################################################################


def reckoning_approval_page(request):
    if request.user.has_perm('APPROVAL'):    
        try:
            reckoningQueueFormPrefix = "reckqueue"
            approveReckoningFormPrefix = "reckapp"
            errors={}
            
            if request.method == 'POST':
                if 'getreck' in request.POST:
                    pendingReckonings = client_get_reckoning_approval_queue(request.user.session_id)
                    reckoningQueueForm = ReckoningQueueForm(request.POST, prefix=reckoningQueueFormPrefix, 
                                                            reckonings=pendingReckonings.reckonings)
                    
                    if (reckoningQueueForm.is_valid()):
                        reckoningId = reckoningQueueForm.cleaned_data.get('pendingselect')
                        request.session["admin_approve_reckoning"] = reckoningId
                    else:
                        for attr, value in reckoningQueueForm.errors.iteritems():
                            errors[attr] = value
                                                      
                elif ('save' in request.POST) or ('approve' in request.POST):
                    approveReckoningForm = ApproveReckoningForm(request.POST, prefix=approveReckoningFormPrefix)
                    
                    if (approveReckoningForm.is_valid()):
                        if (approveReckoningForm.cleaned_data['edit_commentary']):
                            commentary = sanitizeDescriptionHtml(approveReckoningForm.cleaned_data['commentary'].strip())
                            commentary_user_id = request.user.reckoner_id
                        else:
                            commentary = settings.RECKONING_UPDATE_DELETE_SENTINEL
                            commentary_user_id = settings.RECKONING_UPDATE_DELETE_SENTINEL
                            
                        if (approveReckoningForm.cleaned_data['description']):
                            description = sanitizeDescriptionHtml(approveReckoningForm.cleaned_data['description'])
                        else:
                            description = settings.RECKONING_UPDATE_DELETE_SENTINEL
                            
                        answers = [Answer(index=0), Answer(index=1)]
                        for key, attr in approveReckoningForm.cleaned_data.iteritems():
                            if (key.startswith("answer")):
                                index = key.split('_')[1]
                                answers[int(index)-1].text = purgeHtml(attr)
                            elif (key.startswith("subtitle")):
                                index = key.split('_')[1]
                                answers[int(index)-1].subtitle = purgeHtml(attr)

                        savedReckoning=Reckoning(id=request.session["admin_approve_reckoning"],
                                                 question=purgeHtml(approveReckoningForm.cleaned_data['question']),
                                                 description=description,
                                                 answers=answers,
                                                 interval=approveReckoningForm.cleaned_data['interval'],
                                                 highlighted=approveReckoningForm.cleaned_data['highlighted'],
                                                 commentary=commentary,
                                                 commentary_user_id=commentary_user_id,
                                                 tag_csv=purgeHtml(approveReckoningForm.cleaned_data['tags']))
                        
                        response = client_update_reckoning(savedReckoning, request.user.session_id)
                        if (not response.success):
                            logger.error("Error when updating a Reckoning: " + response.message)
                            messages.error(request, "Failed to save reckoning " + request.session["admin_approve_reckoning"])
                        else:
                            messages.info(request, "Saved reckoning " + request.session["admin_approve_reckoning"] + "!")
                    
                        if ('approve' in request.POST):
                            response = client_approve_reckoning(request.session["admin_approve_reckoning"], request.user.session_id)
                            if (not response.success):
                                logger.error("Error when approving a Reckoning: " + response.message)
                                messages.error(request, "Failed to approve reckoning " + request.session["admin_approve_reckoning"])
                            else:
                                messages.info(request, "Approved reckoning " + request.session["admin_approve_reckoning"] + "!")
                                request.session["admin_approve_reckoning"] = None
                    else:
                        for attr, value in approveReckoningForm.errors.iteritems():
                            errors[attr] = value
                    
                elif 'reject' in request.POST:
                    response = client_reject_reckoning(request.session["admin_approve_reckoning"], request.user.session_id)
                    if (not response.success):
                        logger.error("Error when rejecting a Reckoning: " + response.message)
                        messages.error(request, "Failed to approve reckoning " + request.session["admin_approve_reckoning"])
                    else:
                        messages.info(request, "Rejected reckoning " + request.session["admin_approve_reckoning"] + "!")
                        request.session["admin_approve_reckoning"] = None                                              
                        
            pendingReckonings = client_get_reckoning_approval_queue(request.user.session_id)
            reckoningQueueForm = ReckoningQueueForm(prefix=reckoningQueueFormPrefix, reckonings=pendingReckonings.reckonings)            
            
            currentReckoning = None
            approveReckoningForm = None
            postingUser = None
            reckoningId = request.session.get('admin_approve_reckoning', None)
            if (reckoningId):
                reckoningResponse = client_get_reckoning(reckoningId, request.user.session_id, True)
                if (reckoningResponse.status.success and len(reckoningResponse.reckonings) > 0):
                    currentReckoning=reckoningResponse.reckonings[0]
                    postingUser = reckonerauthbackend.get_user(request.user.session_id, currentReckoning.submitter_id)
                    approveReckoningForm = ApproveReckoningForm(prefix=approveReckoningFormPrefix,reckoning=currentReckoning)
                else:
                    request.session['admin_approve_reckoning'] = None
            
            c = RequestContext(request, {'reckoningQueueForm': reckoningQueueForm, 
                                         'approveReckoningForm' : approveReckoningForm,
                                         'currentReckoning' : currentReckoning,
                                         'postingUser' : postingUser,
                                         'errors' : errors})
            
            return render_to_response('approve_reckonings.html', c)            
            
        except Exception:      
            logger.error("Exception when rending reckoning approval screen:") 
            logger.error(traceback.print_exc(8))
            raise Exception
    else:
        return HttpResponseRedirect('/')     


class ReckoningQueueForm(forms.Form):
    def __init__(self, *args, **kwargs):
        reckonings = None
        if ("reckonings" in kwargs):
            reckonings = kwargs.pop("reckonings")
            
        super(ReckoningQueueForm, self).__init__(*args, **kwargs)
        
        reckoningChoices = []
        if (reckonings):
            for reckoning in reckonings:
                reckoningChoices.append((reckoning.id, str(reckoning.submission_date) + " " + str(reckoning.question)))
        
        self.fields["pendingselect"] = forms.ChoiceField(label="Pending Reckonings", choices=reckoningChoices)


class ApproveReckoningForm(forms.Form):
    def __init__(self, *args, **kwargs):
        reckoning = Reckoning(answers = [Answer(index=0), Answer(index=1)])
        
        if ("reckoning" in kwargs):
            reckoning = kwargs.pop("reckoning")
        super(ApproveReckoningForm, self).__init__(*args, **kwargs)
        
        self.fields["question"] = forms.CharField(max_length=150, label="Question", initial=reckoning.question, required=True, widget=forms.Textarea)
        self.fields["description"] = forms.CharField(max_length=3000, label="Description", initial=reckoning.description, required=False, widget=forms.Textarea)
        
        for answer in reckoning.answers:
            self.fields["answer_" + str(int(answer.index)+1)] = forms.CharField(max_length=25, label="Answer " + str(answer.index), initial=answer.text, required=True)
            self.fields["subtitle_" + str(int(answer.index)+1)] = forms.CharField(max_length=25, label="Subtitle " + str(answer.index), initial=answer.subtitle, required=False)

        self.fields["interval"] = forms.DecimalField(max_digits=6, decimal_places=0, label="Interval (in minutes)", initial=reckoning.interval, required=True)
        self.fields["tags"] = forms.CharField(max_length=200, label="Tags", initial=reckoning.getTagCSV(), required=False)
        self.fields["highlighted"] = forms.BooleanField(label="Highlighted", initial=reckoning.highlighted, required=False)
        self.fields["edit_commentary"] = forms.BooleanField(label="Edit Commentary", initial=False, required=False)
        self.fields["commentary"] = forms.CharField(max_length=3000, label="Admin Commentary", initial=reckoning.commentary, required=False, widget=forms.Textarea)
                
            
            