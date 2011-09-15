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
from django.forms.formsets import formset_factory
from django.shortcuts import render_to_response
from django.template import RequestContext

from reckonersite.auth import reckonerauthbackend
from reckonersite.client.facebookclient import client_get_facebook_user_token
from reckonersite.client.googleclient import client_get_google_user_token

logger = logging.getLogger(settings.STANDARD_LOGGER)

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
                        for attr, value in getUserForm.errors:
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
            logger.error("Exception when rending login screen:") 
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

