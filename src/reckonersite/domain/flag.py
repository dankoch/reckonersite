'''
Created on Aug 23, 2011
@author: danko
'''
from xml.etree import cElementTree as cET
from reckonersite.domain.base import Base, buildXml

class Flag(Base):
    '''Object definition of a single flag (as attached to content).  
    Maintained to be synchronized with the Reckoner API'''

    def __init__(self, user_id=None, flag_date=None, reason=None):
        
        # Note: Since we're building the XML nodes off of the names of the attributes,
        # these names need to be kept aligned with the API definition.
        self.id = id
        self.user_id = user_id
        self.flag_date = flag_date
        self.reason = reason
    
    def getXML(self):
        return (buildXml(self.__dict__, 'flag'))
    
    def getXMLString(self):
        return cET.tostring(self.getXML())