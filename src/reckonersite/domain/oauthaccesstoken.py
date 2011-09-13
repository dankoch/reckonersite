'''
Created on Aug 25, 2011
@author: danko
'''
from datetime import datetime
from xml.etree import cElementTree as cET
from reckonersite.domain.base import Base, buildXml, convertToDateTime

class OAuthAccessToken(Base):
    '''Object definition of an Access Token associated with a Facebook User
       Maintained to be synchronized with the Reckoner API's PostOAuthUser (since it's used to post information
    for authentication)'''

    def __init__(self, user_token=None, provider=None, expires=None, refresh_token=None,
                 xml_string=None, xml_element=None):
        
        self.user_token = user_token
        self.expires = expires
        self.provider = provider
        self.refresh_token = refresh_token
        
        if not xml_string is None:
            self.buildFromXMLString(xml_string)
            
        if not xml_element is None:
            self.buildFromXMLElement(xml_element)
    
    def getXML(self):
        return (buildXml(self.__dict__, 'oauth_user_post'))
    
    def getXMLString(self):
        return cET.tostring(self.getXML())

    def buildFromXMLString(self, xml):
        xml_root = cET.XML(xml)
        self.buildFromXMLElement(xml_root)
    
    def buildFromXMLElement(self, xml_root):
        if (not xml_root.find('user_token') is None):
            self.user_token = xml_root.find('user_token').text
        if (not xml_root.find('provider') is None):
            self.provider = xml_root.find('provider').text
        if (not xml_root.find('expires') is None):
            self.expires = xml_root.find('expires').text
        if (not xml_root.find('refresh_token') is None):
            self.refresh_token = xml_root.find('refresh_token').text