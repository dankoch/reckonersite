'''
Created on Oct 17, 2011
@author: danko
'''
from xml.etree import cElementTree as cET
from reckonersite.domain.ajaxserviceresponse import AjaxServiceResponse
from reckonersite.domain.base import Base, buildXml
from reckonersite.domain.reckoning import Reckoning

class ReckoningAjaxResponse(AjaxServiceResponse):
    '''AJAX response for service calls that return a list of reckonings.'''

    def __init__(self, reckonings=None, **kwargs):
        super( ReckoningAjaxResponse, self ).__init__(**kwargs)

        self.reckonings = reckonings
        
    def getXML(self):
        return (buildXml(self.__dict__, 'reckoning_ajax_response'))
    
    def getXMLString(self):
        return cET.tostring(self.getXML())
    
    def buildFromXMLString(self, xml):
        xml_root = cET.XML(xml)
        self.buildFromXMLElement(xml_root)
    
    def buildFromXMLElement(self, xml_root):
        super( ReckoningAjaxResponse, self ).buildFromXMLElement(self, xml_root)
        
        reckoningsElement = xml_root.find('reckonings')
        if (not reckoningsElement is None):
            self.reckonings = []
            for reckoningElement in reckoningsElement.findall('reckoning'):
                self.reckonings.append(Reckoning(xml_element=reckoningElement))