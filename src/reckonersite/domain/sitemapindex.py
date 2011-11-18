'''
Created on Nov 16, 2011
@author: danko
'''
from datetime import datetime
from xml.etree import cElementTree as cET
from reckonersite.domain.base import Base, buildXml, convertToDateTime
from reckonersite.domain.sitemapdoc import SiteMapDoc

class SiteMapIndex(Base):
    '''Object definition of a Sitemap index document used for search engine traversal.'''

    def __init__(self, sitemaps=None,
                 xml_string=None, xml_element=None):
        
        self.sitemaps = sitemaps
        
        if not xml_string is None:
            self.buildFromXMLString(xml_string)
            
        if not xml_element is None:
            self.buildFromXMLElement(xml_element)
        
    def getXML(self):
        selfdoc = buildXml(self.sitemaps, 'sitemapindex')
        selfdoc.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        
        return selfdoc
    
    def getXMLString(self):
        return ("\n".join(('<?xml version=\"1.0\" encoding=\"UTF-8\"?>',cET.tostring(self.getXML()),)))
    
    def buildFromXMLString(self, xml):
        xml_root = cET.XML(xml)
        self.buildFromXMLElement(xml_root)
    
    def buildFromXMLElement(self, xml_root):
        self.sitemaps=[]
        for sitemapElement in xml_root.findall('sitemap'):
            self.sitemaps.append(SiteMapDoc(xml_element=sitemapElement))
