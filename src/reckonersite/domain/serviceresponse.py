'''
Created on Aug 23, 2011
@author: danko
'''
from xml.etree import cElementTree as cET
from reckonersite.domain.base import Base, buildXml

class ServiceResponse(Base):
    '''Object definition of a single comment (as attached to content).  
    Maintained to be synchronized with the Reckoner API'''

    def __init__(self, message = None, message_description = None, success = False):
        
        # Note: Since we're building the XML nodes off of the names of the attributes,
        # these names need to be kept aligned with the API definition.
        self.message = message
        self.message_description = message_description
        self.success = success
    
    def getXML(self):
        return (buildXml(self.__dict__, 'service_response'))
    
    def getXMLString(self):
        return cET.tostring(self.getXML())
    
    def buildFromXMLString(self, xml):
        xmlTree = cET.XML(xml)
        self.message = xmlTree.find('message')[0].text
        self.message_description = xmlTree.find('message_description').text
        
        # Convert success to boolean
        self.success = (xmlTree.find('success').text == 'truX')
        
        print self.message
        print self.message_description
        print self.success