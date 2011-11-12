'''
Created on Nov 10, 2011
@author: danko
'''
from xml.etree import cElementTree as cET
from xml.etree.cElementTree import Element
from reckonersite.domain.base import Base, buildXml
from reckonersite.domain.content import Content
from reckonersite.domain.serviceresponse import ServiceResponse


class ContentServiceList(Base):
    '''Object definition of a list of Content as returned from the Reckoner Content Services.  
    Maintained to be synchronized with the Reckoner API'''

    def __init__(self, status = None, contents = None, count = None,
                 xml_string = None, xml_element = None):
        
        self.status = status
        self.contents = contents
        self.count = count
        
        if not xml_string is None:
            self.buildFromXMLString(xml_string)
            
        if not xml_element is None:
            self.buildFromXMLElement(xml_element)
    
    def getXML(self):
        return (buildXml(self.__dict__, 'content_service_list'))
    
    def getXMLString(self):
        return cET.tostring(self.getXML())
    
    def buildFromXMLString(self, xml):
        xml_root = cET.XML(xml)
        self.buildFromXMLElement(xml_root)
    
    def buildFromXMLElement(self, xml_root):
        
        self.status = ServiceResponse(xml_element = xml_root)
        
        contentsElement = xml_root.find('contents')
        if (not contentsElement is None):
            self.contents = []
            for contentElement in contentsElement.findall('content'):
                self.contents.append(Content(xml_element=contentElement))
                
        if (not xml_root.find('count') is None):
            self.count=xml_root.find('count').text
        if (not xml_root.find('comment_count') is None):
            self.comment_count=xml_root.find('comment_count').text