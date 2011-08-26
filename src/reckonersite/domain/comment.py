'''
Created on Aug 23, 2011
@author: danko
'''
from xml.etree import cElementTree as cET
from reckonersite.domain.base import Base, buildXml

class Comment(Base):
    '''Object definition of a single comment (as attached to content).  
    Maintained to be synchronized with the Reckoner API'''

    def __init__(self, id=None, comment=None, poster_id=None, posting_date=None,
                 favorites=None, flags=None):
        
        # Note: Since we're building the XML nodes off of the names of the attributes,
        # these names need to be kept aligned with the API definition.
        self.id = id
        self.comment = comment
        self.poster_id = poster_id
        self.posting_date = posting_date
        self.favorites = favorites
        self.flags = flags
    
    def getXML(self):
        return (buildXml(self.__dict__, 'comment'))
    
    def getXMLString(self):
        return cET.tostring(self.getXML())