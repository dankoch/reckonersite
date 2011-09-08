'''
Created on Sept 4, 2011
@author: danko
'''
from xml.etree import cElementTree as cET
from xml.etree.cElementTree import Element
from reckonersite.domain.base import Base, buildXml
from reckonersite.domain.authsession import AuthSession
from reckonersite.domain.reckoneruser import ReckonerUser
from reckonersite.domain.serviceresponse import ServiceResponse

class UserServiceResponse(Base):
    '''Object definition of a the authentication-related information provided by the Reckoner Content Services.  
    Maintained to be synchronized with the Reckoner API'''

    def __init__(self, status = None, reckoner_user = None, auth_session = None,
                 xml_string = None, xml_element = None):
        
        self.status = status
        self.reckoner_user = reckoner_user
        self.auth_session = auth_session
        
        if not xml_string is None:
            self.buildFromXMLString(xml_string)
            
        if not xml_element is None:
            self.buildFromXMLElement(xml_element)
    
    def getXML(self):
        return (buildXml(self.__dict__, 'reckonings_service_list'))
    
    def getXMLString(self):
        return cET.tostring(self.getXML())
    
    def buildFromXMLString(self, xml):
        xml_root = cET.XML(xml)
        self.buildFromXMLElement(xml_root)
    
    def buildFromXMLElement(self, xml_root):
        
        self.status = ServiceResponse(xml_element = xml_root)
        
        userElement = xml_root.find('user')
        if (not userElement is None):
            self.reckoner_user = ReckonerUser(xml_element = userElement)
            
        sessionElement = xml_root.find('auth_session')
        if (not sessionElement is None):
            self.auth_session = AuthSession(xml_element = sessionElement)        