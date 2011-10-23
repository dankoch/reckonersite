'''
Created on Aug 26, 2011
@author: danko
'''
from xml.etree import cElementTree as cET
from xml.etree.cElementTree import Element
from reckonersite.domain.base import Base, buildXml
from reckonersite.domain.reckoning import Reckoning
from reckonersite.domain.serviceresponse import ServiceResponse


class ReckoningServiceList(Base):
    '''Object definition of a list of Reckonings as returned from the Reckoner Content Services.  
    Maintained to be synchronized with the Reckoner API'''

    def __init__(self, status = None, reckonings = None, count = None, 
                 xml_string = None, xml_element = None):
        
        self.status = status
        self.reckonings = reckonings
        self.count = count
        
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
        
        reckoningsElement = xml_root.find('reckonings')
        if (not reckoningsElement is None):
            self.reckonings = []
            for reckoningElement in reckoningsElement.findall('reckoning'):
                self.reckonings.append(Reckoning(xml_element=reckoningElement))
                
        if (not xml_root.find('count') is None):
            self.count=xml_root.find('count').text