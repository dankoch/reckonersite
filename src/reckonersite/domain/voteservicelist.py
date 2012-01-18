'''
Created on Aug 26, 2011
@author: danko
'''
from xml.etree import cElementTree as cET
from xml.etree.cElementTree import Element
from reckonersite.domain.base import Base, buildXml
from reckonersite.domain.serviceresponse import ServiceResponse
from reckonersite.domain.vote import Vote


class VoteServiceList(Base):
    '''Object definition of a list of Reckonings as returned from the Reckoner Content Services.  
    Maintained to be synchronized with the Reckoner API'''

    def __init__(self, status = None, votes = None, success = False, 
                 count = None,
                 xml_string = None, xml_element = None):
        
        self.status = status
        self.votes = votes
        self.count = count
        
        if not xml_string is None:
            self.buildFromXMLString(xml_string)
            
        if not xml_element is None:
            self.buildFromXMLElement(xml_element)
    
    def getXML(self):
        return (buildXml(self.__dict__, 'vote_service_list'))
    
    def getXMLString(self):
        return cET.tostring(self.getXML())
    
    def buildFromXMLString(self, xml):
        xml_root = cET.XML(xml)
        self.buildFromXMLElement(xml_root)
    
    def buildFromXMLElement(self, xml_root):
        
        self.status = ServiceResponse(xml_element = xml_root)
        
        votesElement = xml_root.find('votes')
        if (not votesElement is None):
            self.votes = []
            for voteElement in votesElement.findall('vote'):
                self.votes.append(Vote(xml_element=voteElement))
        if (not xml_root.find('count') is None):
            self.count=xml_root.find('count').text