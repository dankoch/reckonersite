'''
Created on Aug 23, 2011
@author: danko
'''
from datetime import datetime
from xml.etree import cElementTree as cET
from reckonersite.domain.base import Base, buildXml, convertToDateTime
from reckonersite.domain.favorite import Favorite
from reckonersite.domain.flag import Flag

class Comment(Base):
    '''Object definition of a single comment (as attached to content).  
    Maintained to be synchronized with the Reckoner API'''

    def __init__(self, id=None, comment=None, poster_id=None, posting_date=None,
                 favorites=None, flags=None, xml_string=None, xml_element=None):
        
        # Note: Since we're building the XML nodes off of the names of the attributes,
        # these names need to be kept aligned with the API definition.
        self.id = id
        self.comment = comment
        self.poster_id = poster_id
        self.posting_date = posting_date
        self.favorites = favorites
        self.flags = flags
        
        if not xml_string is None:
            self.buildFromXMLString(xml_string)
            
        if not xml_element is None:
            self.buildFromXMLElement(xml_element)
    
    def getXML(self):
        return (buildXml(self.__dict__, 'comment'))
    
    def getXMLString(self):
        return cET.tostring(self.getXML())
    
    def buildFromXMLString(self, xml):
        xml_root = cET.XML(xml)
        self.buildFromXMLElement(xml_root)
    
    def buildFromXMLElement(self, xml_root):
        if (not xml_root.find('id') is None):
            self.id = xml_root.find('id').text
        if (not xml_root.find('comment') is None):
            self.comment = xml_root.find('comment').text
        if (not xml_root.find('poster_id') is None):
            self.poster_id = xml_root.find('poster_id').text
        
        if (not xml_root.find('posting_date') is None) and (not xml_root.find('posting_date').text is None):
            self.posting_date = convertToDateTime(xml_root.find('posting_date').text)
        
        flagsElement = xml_root.find('flags')        
        if (not flagsElement is None):
            self.flags=[]
            for flagElement in flagsElement.findall('flags'):
                self.flags.append(Flag(xml_element=flagElement))
        
        favoritesElement = xml_root.find('favorites')
        if (not favoritesElement is None):               
            self.favorites=[]
            for favoriteElement in favoritesElement.findall('favorite'):
                self.favorites.append(Favorite(xml_element=favoriteElement))        