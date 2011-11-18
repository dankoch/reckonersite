'''
Created on Nov 16, 2011
@author: danko
'''
from datetime import datetime
from xml.etree import cElementTree as cET
from reckonersite.domain.base import Base, buildXml, convertToDateTime

class SiteMapUrl(Base):
    '''Object definition of an individual URL used within a Sitemap document'''

    def __init__(self, loc=None, lastmod=None, changefreq=None, priority=None,
                 xml_string=None, xml_element=None):
        
        self.loc = loc
        self.lastmod = lastmod
        self.changefreq = changefreq
        self.priority = priority
        
        if not xml_string is None:
            self.buildFromXMLString(xml_string)
            
        if not xml_element is None:
            self.buildFromXMLElement(xml_element)
        
    def getXML(self):
        return (buildXml(self.__dict__, 'url'))
    
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
            
        if (not xml_root.find('changefreq') is None):
            self.changefreq = xml_root.find('changefreq').text
        if (not xml_root.find('priority') is None):
            self.priority = xml_root.find('priority').text
