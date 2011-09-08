'''
Created on Sept 4, 2011
@author: danko
'''
from datetime import datetime
from xml.etree import cElementTree as cET
from reckonersite.domain.base import Base, buildXml, convertToDateTime

class AuthSession(Base):
    '''Object definition of an authentication session (as defined in the Reckoner DB)  
    Maintained to be synchronized with the Reckoner API'''

    def __init__(self, user_token=None, reckoner_user_id=None, auth_provider=None,
                 created_date=None, expiration_date=None,
                 xml_string=None, xml_element=None):
        
        # Note: Since we're building the XML nodes off of the names of the attributes,
        # these names need to be kept aligned with the API definition.
        self.user_token = user_token
        self.reckoner_user_id = reckoner_user_id
        self.auth_provider = auth_provider
        self.created_date = created_date
        self.expiration_date = expiration_date
        
        if not xml_string is None:
            self.buildFromXMLString(xml_string)
            
        if not xml_element is None:
            self.buildFromXMLElement(xml_element)
    
    def getXML(self):
        return (buildXml(self.__dict__, 'auth_session'))
    
    def getXMLString(self):
        return cET.tostring(self.getXML())
    
    def buildFromXMLString(self, xml):
        xml_root = cET.XML(xml)
        self.buildFromXMLElement(xml_root)
    
    def buildFromXMLElement(self, xml_root):
        if (not xml_root.find('user_token') is None):
            self.user_token = xml_root.find('user_token').text
        if (not xml_root.find('reckoner_user_id') is None):
            self.reckoner_user_id = xml_root.find('reckoner_user_id').text
        if (not xml_root.find('auth_provider') is None):
            self.first_name = xml_root.find('auth_provider').text
        
        if (not xml_root.find('created_date') is None) and (not xml_root.find('created_date').text is None):
            self.created_date = convertToDateTime(xml_root.find('created_date').text)

        if (not xml_root.find('expiration_date') is None) and (not xml_root.find('expiration_date').text is None):
            self.expiration_date = convertToDateTime(xml_root.find('expiration_date').text)     