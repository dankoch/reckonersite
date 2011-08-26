'''
Created on Aug 23, 2011
@author: danko
'''
from xml.etree import cElementTree as cET
from reckonersite.domain.base import Base, buildXml

class Answer(Base):
    '''Object definition of a single answer (as commonly attached to a Reckoning).  
    Maintained to be synchronized with the Reckoner API'''

    def __init__(self, index=None, text=None, subtitle=None, vote_total=None, votes=None):
        
        # Note: Since we're building the XML nodes off of the names of the attributes,
        # these names need to be kept aligned with the API definition.
        self.index = index
        self.text = text
        self.subtitle = subtitle
        self.vote_total = vote_total
        self.votes = votes
        
    def getXML(self):
        return (buildXml(self.__dict__, 'answer'))
    
    def getXMLString(self):
        return cET.tostring(self.getXML())