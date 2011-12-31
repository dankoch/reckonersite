'''
Created on Dec 22, 2011
@author: danko
'''
from xml.etree import cElementTree as cET
from reckonersite.domain.base import Base, buildXml, convertToDateTime

class Media(Base):
    '''Object definition of a basic media item.  Maintained to be synchronized with the Reckoner API'''

    def __init__(self, media_id=None, media_type=None, name=None, url=None,
                 file_type=None, duration=None, size=None,
                 xml_string=None, xml_element=None):

        self.media_id = media_id
        self.media_type = media_type
        self.name = name
        self.url = url
        self.file_type = file_type
        self.duration = duration
        self.size = size
        
        if not xml_string is None:
            self.buildFromXMLString(xml_string)
            
        if not xml_element is None:
            self.buildFromXMLElement(xml_element)
        
    def getXML(self):
        return (buildXml(self.__dict__, 'media'))
    
    def getXMLString(self):
        return cET.tostring(self.getXML())
    
    def buildFromXMLString(self, xml):
        xml_root = cET.XML(xml)
        self.buildFromXMLElement(xml_root)
    
    def buildFromXMLElement(self, xml_root):
        if (not xml_root.find('media_id') is None):
            self.media_id = xml_root.find('media_id').text
        if (not xml_root.find('media_type') is None):
            self.media_type = xml_root.find('media_type').text
        if (not xml_root.find('name') is None):
            self.name = xml_root.find('name').text
        if (not xml_root.find('url') is None):
            self.url = xml_root.find('url').text
        if (not xml_root.find('file_type') is None):
            self.file_type = xml_root.find('file_type').text
        if (not xml_root.find('duration') is None):
            self.duration = xml_root.find('duration').text
        if (not xml_root.find('size') is None):
            self.size = xml_root.find('size').text