'''
Created on Nov 16, 2011
@author: danko
'''
from datetime import datetime
from xml.etree import cElementTree as cET
from reckonersite.domain.base import Base, buildXml, convertToDateTime
from reckonersite.domain.sitemapurl import SiteMapUrl

class SiteMap(Base):
    '''Object definition of a Sitemap document used for search engine traversal.'''

    def __init__(self, urls=None,
                 xml_string=None, xml_element=None):
        
        self.urls = urls
        
        if not xml_string is None:
            self.buildFromXMLString(xml_string)
            
        if not xml_element is None:
            self.buildFromXMLElement(xml_element)
        
    def getXML(self):
        selfdoc = buildXml(self.urls, 'urlset')
        selfdoc.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        
        return selfdoc
    
    def getXMLString(self):
        return ("\n".join(('<?xml version=\"1.0\" encoding=\"UTF-8\"?>',cET.tostring(self.getXML()),)))
    
    def buildFromXMLString(self, xml):
        xml_root = cET.XML(xml)
        self.buildFromXMLElement(xml_root)
    
    def buildFromXMLElement(self, xml_root):     
        self.urls=[]
        for urlElement in xml_root.findall('url'):
            self.urls.append(SiteMapUrl(xml_element=urlElement))
