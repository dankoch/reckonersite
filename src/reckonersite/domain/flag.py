'''
Created on Aug 23, 2011
@author: danko
'''
from datetime import datetime
from xml.etree import cElementTree as cET
from reckonersite.domain.base import Base, buildXml, convertToDateTime

class Flag(Base):
    '''Object definition of a single flag (as attached to content).  
    Maintained to be synchronized with the Reckoner API'''

    def __init__(self, user_id=None, flag_date=None, reason=None, xml_string=None, xml_element=None):
        
        # Note: Since we're building the XML nodes off of the names of the attributes,
        # these names need to be kept aligned with the API definition.
        self.id = id
        self.user_id = user_id
        self.flag_date = flag_date
        self.reason = reason
                
        if not xml_string is None:
            self.buildFromXMLString(xml_string)
            
        if not xml_element is None:
            self.buildFromXMLElement(xml_element)
    
    def getXML(self):
        return (buildXml(self.__dict__, 'flag'))
    
    def buildFromXMLString(self, xml):
        xml_root = cET.XML(xml)
        self.buildFromXMLElement(xml_root)
    
    def buildFromXMLElement(self, xml_root):
        if (not xml_root.find('id') is None): 
            self.id = xml_root.find('id').text
        if (not xml_root.find('user_id') is None): 
            self.user_id = xml_root.find('user_id').text
        if (not xml_root.find('flag_date') is None) and (not xml_root.find('flag_date').text is None):
            self.flag_date = convertToDateTime(xml_root.find('flag_date').text)
        if (not xml_root.find('reason') is None): 
            self.reason = xml_root.find('reason').text