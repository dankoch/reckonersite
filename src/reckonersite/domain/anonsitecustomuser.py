'''
Created on Sep 5, 2011
@author: danko
'''
from reckonersite.domain.sitecustomuser import SiteCustomUser

class AnonSiteCustomUser(SiteCustomUser):
    '''
    Object representing an anonymous user.  Initialization data is fixed to
    indicate the default user permissions (should be aligned w/ Reckoner API)
    '''
    
    def __init__(self, session_id=None):
        
        self.reckoner_id = 'anon'
        self.username = 'anon'
        self.first_name = None
        self.last_name = None
        self.email = None
        self.auth_provider = None
        self.auth_provider_id = None
        self.first_login = None
        self.last_login = None
        self.profile_picture_url = None
        self.profile_url = None
        
        # Default permissions for anonymous users.  Reckon Site will
        # vouch for anonymous 
        self.groups = ['ANON']
        self.permissions = ['vote']
        self.active = True
        
        self.session_id = session_id
        self.expires = None
        
        self.is_anonymous = True   