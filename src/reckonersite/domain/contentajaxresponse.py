'''
Created on Oct 17, 2011
@author: danko
'''
from xml.etree import cElementTree as cET
from reckonersite.domain.ajaxserviceresponse import AjaxServiceResponse
from reckonersite.domain.base import Base, buildXml
from reckonersite.domain.content import Content

class ContentAjaxResponse(AjaxServiceResponse):
    '''AJAX response for service calls that return a list of content.'''

    def __init__(self, contents=None, **kwargs):
        super( ContentAjaxResponse, self ).__init__(**kwargs)

        self.contents = contents
        
    def getXML(self):
        return (buildXml(self.__dict__, 'content_ajax_response'))
    
    def getXMLString(self):
        return cET.tostring(self.getXML())
    
    def buildFromXMLString(self, xml):
        xml_root = cET.XML(xml)
        self.buildFromXMLElement(xml_root)
    
    def buildFromXMLElement(self, xml_root):
        super( ContentAjaxResponse, self ).buildFromXMLElement(self, xml_root)
        
        contentsElement = xml_root.find('contents')
        if (not contentsElement is None):
            self.contents = []
            for contentElement in contentsElement.findall('content'):
                self.reckonings.append(Content(xml_element=contentElement))