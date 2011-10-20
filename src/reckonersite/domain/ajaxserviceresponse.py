'''
Created on Oct 17, 2011
@author: danko
'''
from xml.etree import cElementTree as cET
from reckonersite.domain.base import Base, buildXml

class AjaxServiceResponse(Base):
    '''Object definition of the response provided to an AJAX call.'''

    def __init__(self, message = None, message_description = None, success = False, 
                 xml_string = None, xml_element = None):
        
        # Note: Since we're building the XML nodes off of the names of the attributes,
        # these names need to be kept aligned with the API definition.
        self.message = message
        self.message_description = message_description
        self.success = success
        
        if not xml_string is None:
            self.buildFromXMLString(xml_string)
            
        if not xml_element is None:
            self.buildFromXMLElement(xml_element)
    
    def getXML(self):
        return (buildXml(self.__dict__, 'ajax_service_response'))
    
    def getXMLString(self):
        return cET.tostring(self.getXML())
    
    def buildFromXMLString(self, xml):
        xml_root = cET.XML(xml)
        self.buildFromXMLElement(xml_root)
    
    def buildFromXMLElement(self, xml_root):
        if (not xml_root.find('message') is None):
            self.message = xml_root.find('message')[0].text
        if (not xml_root.find('message_description') is None):
            self.message_description = xml_root.find('message_description').text
        
        # Convert success to boolean
        if (not xml_root.find('success') is None):
            self.success = (xml_root.find('success').text == 'true')