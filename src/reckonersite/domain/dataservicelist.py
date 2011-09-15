'''
Created on Aug 26, 2011
@author: danko
'''
from xml.etree import cElementTree as cET
from xml.etree.cElementTree import Element
from reckonersite.domain.base import Base, buildXml
from reckonersite.domain.reckoning import Reckoning
from reckonersite.domain.serviceresponse import ServiceResponse


class DataServiceList(Base):
    '''Object definition of a list of String data returned from the Reckoner Content Services.  
    Maintained to be synchronized with the Reckoner API'''

    def __init__(self, status = None, data = None, success = False, 
                 xml_string = None, xml_element = None):
        
        self.status = status
        self.data = data
        
        if not xml_string is None:
            self.buildFromXMLString(xml_string)
            
        if not xml_element is None:
            self.buildFromXMLElement(xml_element)
    
    def getXML(self):
        return (buildXml(self.__dict__, 'data_service_list'))
    
    def getXMLString(self):
        return cET.tostring(self.getXML())
    
    def buildFromXMLString(self, xml):
        xml_root = cET.XML(xml)
        self.buildFromXMLElement(xml_root)
    
    def buildFromXMLElement(self, xml_root):
        
        self.status = ServiceResponse(xml_element = xml_root)
        
        dataElement = xml_root.find('data')
        if (not dataElement is None):
            self.data = []
            for datumElement in dataElement.findall('item'):
                self.data.append(datumElement.text)