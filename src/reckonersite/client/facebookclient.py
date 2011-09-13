'''
Created on Aug 25, 2011
@author: danko
'''
import urllib2
from urlparse import urlparse

from django.conf import settings
from reckonersite.domain.oauthaccesstoken import OAuthAccessToken

def client_get_facebook_user_token(code):
    url = settings.FACEBOOK_GRAPH_TOKEN_URL + "?client_id=" + settings.FACEBOOK_APP_ID \
                                            + "&redirect_uri=" + settings.FACEBOOK_REDIRECT_URL \
                                            + "&client_secret=" + settings.FACEBOOK_APP_SECRET \
                                            + "&code=" + code
        
    response = urllib2.urlopen(url)    
    content = response.read()
    params = dict([part.split('=') for part in content.split('&')])
    
    oAuthReceipt = OAuthAccessToken()
    if params.has_key('access_token'):
        oAuthReceipt.user_token = params['access_token']
    if params.has_key('expires'):
        oAuthReceipt.expires = params['expires']
    oAuthReceipt.provider = 'FACEBOOK'
    
    return oAuthReceipt
    
    
    
        