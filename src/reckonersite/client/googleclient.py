'''
Created on Aug 25, 2011
@author: danko
'''
from json import JSONDecoder
import urllib
import urllib2
from urlparse import urlparse

from django.conf import settings
from reckonersite.domain.oauthaccesstoken import OAuthAccessToken

def client_get_google_user_token(code):
    url = settings.GOOGLE_API_TOKEN_URL
    
    post_values = (("code", code),
                   ("client_id", settings.GOOGLE_APP_ID),
                   ("client_secret", settings.GOOGLE_APP_SECRET),
                   ("redirect_uri", settings.GOOGLE_REDIRECT_URL),
                   ("grant_type", "authorization_code"))
    
    post_data = urllib.urlencode(post_values)
    
    req = urllib2.Request(url = url,
                          data = post_data)
    
    response = urllib2.urlopen(req)
    decoder = JSONDecoder()
    response_content = decoder.decode(response.read())
    
    oAuthReceipt = OAuthAccessToken()
    if response_content.has_key('access_token'):
        oAuthReceipt.user_token = response_content['access_token']
    if response_content.has_key('expires_in'):
        oAuthReceipt.expires = response_content['expires_in']
    if response_content.has_key('refresh_token'):
        oAuthReceipt.refresh_token = response_content['refresh_token']

    oAuthReceipt.provider = 'GOOGLE'
    
    return oAuthReceipt
    
    
    
        