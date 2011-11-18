'''
Created on Nov 16, 2011
@author: danko
'''
from datetime import datetime
from xml.etree import cElementTree as cET
from reckonersite.domain.base import Base, buildXml, convertToDateTime

class SiteMapDoc(Base):
    '''Object definition of a Sitemap document within a Sitemap Index file'''

    def __init__(self, loc=None, lastmod=None,
                 xml_string=None, xml_element=None):
        
        self.loc = loc
        self.lastmod = lastmod
        
        if not xml_string is None:
            self.buildFromXMLString(xml_string)
            
        if not xml_element is None:
            self.buildFromXMLElement(xml_element)
        
    def getXML(self):
        return (buildXml(self.__dict__, 'sitemap'))
    
    def getXMLString(self):
        return cET.tostring(self.getXML())
    
    def buildFromXMLString(self, xml):
        xml_root = cET.XML(xml)
        self.buildFromXMLElement(xml_root)
    
    def buildFromXMLElement(self, xml_root):
        if (not xml_root.find('loc') is None):
            self.loc = xml_root.find('loc').text
        if (not xml_root.find('lastmod') is None) and (not xml_root.find('lastmod').text is None):
            self.lastmod = convertToDateTime(xml_root.find('lastmod').text)
