'''
Created on Aug 26, 2011
@author: danko
'''
from xml.etree import cElementTree as cET
from xml.etree.cElementTree import Element
from reckonersite.domain.base import Base, buildXml
from reckonersite.domain.serviceresponse import ServiceResponse


class TagServiceList(Base):
    '''Object definition of a list of Reckonings as returned from the Reckoner Content Services.  
    Maintained to be synchronized with the Reckoner API'''

    def __init__(self, status = None, tags = None,
                 xml_string = None, xml_element = None):
        
        self.status = status
        self.tags = tags
        
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
        
        tagsElement = xml_root.find('tags')
        if (not tagsElement is None):
            self.tags = []
            for tagElement in tagsElement.findall('tag'):
                self.tags.append(Tag(xml_element=tagElement))
            
class Tag(Base):
    def __init__(self, tag=None, count=0,
                 xml_string = None, xml_element = None):
        self.tag = tag
        self.count = count
        
        if not xml_string is None:
            self.buildFromXMLString(xml_string)
            
        if not xml_element is None:
            self.buildFromXMLElement(xml_element)
        
    def getXML(self):
        return (buildXml(self.tag, 'tag'))
    
    def getXMLString(self):
        return cET.tostring(self.getXML())    
    
    def buildFromXMLString(self, xml):
        xml_root = cET.XML(xml)
        self.buildFromXMLElement(xml_root)
    
    def buildFromXMLElement(self, xml_root):
        
        self.status = ServiceResponse(xml_element = xml_root)
        
        if (not xml_root.find('tag') is None):            
            self.tag = xml_root.find('tag').text
        if (not xml_root.find('count') is None):
            self.count = xml_root.find('count').text