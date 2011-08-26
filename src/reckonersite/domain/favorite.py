'''
Created on Aug 23, 2011
@author: danko
'''
from xml.etree import cElementTree as cET
from reckonersite.domain.base import Base, buildXml

class Favorite(Base):
    '''Object definition of a single favorite (as attached to content).  
    Maintained to be synchronized with the Reckoner API'''

    def __init__(self, user_id=None, favorite_date=None):
        
        # Note: Since we're building the XML nodes off of the names of the attributes,
        # these names need to be kept aligned with the API definition.
        self.user_id = user_id
        self.favorite_date = favorite_date
    
    def getXML(self):
        return (buildXml(self.__dict__, 'favorite'))
    
    def getXMLString(self):
        return cET.tostring(self.getXML())