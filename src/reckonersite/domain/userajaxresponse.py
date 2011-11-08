'''
Created on Oct 17, 2011
@author: danko
'''
from xml.etree import cElementTree as cET
from reckonersite.domain.ajaxserviceresponse import AjaxServiceResponse
from reckonersite.domain.base import Base, buildXml
from reckonersite.domain.reckoneruser import ReckonerUser

class UserAjaxResponse(AjaxServiceResponse):
    '''AJAX response for service calls that return a user.'''

    def __init__(self, reckoner_user=None, **kwargs):
        super( UserAjaxResponse, self ).__init__(**kwargs)

        self.reckoner_user = reckoner_user
        
    def getXML(self):
        return (buildXml(self.__dict__, 'user_ajax_response'))
    
    def getXMLString(self):
        return cET.tostring(self.getXML())
    
    def buildFromXMLString(self, xml):
        xml_root = cET.XML(xml)
        self.buildFromXMLElement(xml_root)
    
    def buildFromXMLElement(self, xml_root):
        super( UserAjaxResponse, self ).buildFromXMLElement(self, xml_root)
        
        userElement = xml_root.find('user')
        if (not userElement is None):
            self.reckoner_user = ReckonerUser(xml_element = userElement)