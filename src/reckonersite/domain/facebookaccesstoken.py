'''
Created on Aug 25, 2011
@author: danko
'''
from datetime import datetime
from xml.etree import cElementTree as cET
from reckonersite.domain.base import Base, buildXml, convertToDateTime

class FacebookAccessToken(Base):
    '''Object definition of an Access Token associated with a Facebook User'''

    def __init__(self, access_token=None, expires=None, 
                 xml_string=None, xml_element=None):
        
        self.access_token = access_token
        self.expires = expires
        
        if not xml_string is None:
            self.buildFromXMLString(xml_string)
            
        if not xml_element is None:
            self.buildFromXMLElement(xml_element)
    
    def getXML(self):
        return (buildXml(self.__dict__, 'facebook_access_token'))
    
    def getXMLString(self):
        return cET.tostring(self.getXML())

    def buildFromXMLString(self, xml):
        xml_root = cET.XML(xml)
        self.buildFromXMLElement(xml_root)
    
    def buildFromXMLElement(self, xml_root):
        if (not xml_root.find('access_token') is None):
            self.access_token = xml_root.find('access_token').text
        if (not xml_root.find('expires') is None):
            self.expires = xml_root.find('expires').text