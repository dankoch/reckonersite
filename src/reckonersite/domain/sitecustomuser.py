'''
Created on Sep 5, 2011
@author: danko
'''

from reckonersite.util.validation import slugifyTitle

class SiteCustomUser(object):
    '''
    Represents the user model used throughout Reckonersite.  Most of the information
    maps directly against the Reckonuser object (which is aligned with the Reckoner Services API),
    but this is its own object for any custom fields the site needs.
    '''
    
    def __init__(self, reckoner_id=None, username=None, first_name=None, last_name=None, email=None,
                 auth_provider=None, auth_provider_id=None, first_login=None, last_login=None, 
                 profile_picture_url=None, profile_url=None, groups=None, permissions=None,
                 active=False, session_id=None, expiration_date=None, is_new_user=False,
                 is_anonymous=False, is_invalid_google_user=False,
                 reckoner_user=None, auth_session=None):
        
        self.reckoner_id = reckoner_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.auth_provider = auth_provider
        self.auth_provider_id = auth_provider_id
        self.first_login = first_login
        self.last_login = last_login
        self.profile_picture_url = profile_picture_url
        self.profile_url = profile_url
        self.groups = groups
        self.permissions = permissions
        self.active = active
        
        self.session_id = session_id
        self.expiration_date = expiration_date
        
        self.is_new_user = is_new_user
        self.is_anonymous = is_anonymous
        self.is_invalid_google_user = is_invalid_google_user
        
        if (reckoner_user):
            self.build_from_reckonuser(reckoner_user)
        if (auth_session):
            self.build_from_authsession(auth_session)
    
    def build_from_reckonuser (self, reckonerUser):
        '''
        Converts a user from the Reckoner Services to the User object used within Reckoner Site
        '''
        self.reckoner_id = reckonerUser.id
        self.username = reckonerUser.username
        self.first_name = reckonerUser.first_name
        self.last_name = reckonerUser.last_name
        self.email = reckonerUser.email
        self.auth_provider = reckonerUser.auth_provider
        self.auth_provider_id = reckonerUser.auth_provider_id
        self.first_login = reckonerUser.first_login
        self.last_login = reckonerUser.last_login
        self.profile_picture_url = reckonerUser.profile_picture_url
        self.profile_url = reckonerUser.profile_url
        self.groups = reckonerUser.groups
        self.permissions = reckonerUser.permissions
        self.active = reckonerUser.active
        
    def build_from_authsession (self, authSession):
        '''
        Extracts the AuthSession data from the Reckoner Services into the User object used within Reckoner Site
        '''        
        self.session_id = authSession.session_id
        self.expiration_date = authSession.expiration_date
        
    def has_perm (self, permission):
        if (self.permissions) and (self.active):
            return permission in self.permissions
        else:
            return False
        
    def has_group (self, group):
        if (self.groups):
            return group in self.groups
        else:
            return False     
        
    def getURL(self):
        if (self.reckoner_id and self.first_name):
            return '/user/' + self.reckoner_id + "/" + slugifyTitle(self.first_name + " " + self.last_name)
        
        return None   