'''
Created on Aug 23, 2011
@author: danko
'''
from xml.etree import cElementTree as cET
from reckonersite.domain.base import Base, buildXml
from reckonersite.domain.vote import Vote

class Answer(Base):
    '''Object definition of a single answer (as commonly attached to a Reckoning).  
    Maintained to be synchronized with the Reckoner API'''

    def __init__(self, index=None, text=None, subtitle=None, vote_total=None, votes=None, percentage=None,
                 xml_string=None, xml_element=None):
        
        # Note: Since we're building the XML nodes off of the names of the attributes,
        # these names need to be kept aligned with the API definition.
        self.index = index
        self.text = text
        self.subtitle = subtitle
        self.vote_total = vote_total
        self.votes = votes
        self.percentage = percentage
        
        if not xml_string is None:
            self.buildFromXMLString(xml_string)
            
        if not xml_element is None:
            self.buildFromXMLElement(xml_element)
        
    def getXML(self):
        return (buildXml(self.__dict__, 'answer'))
    
    def getXMLString(self):
        return cET.tostring(self.getXML())
    
    def buildFromXMLString(self, xml):
        xml_root = cET.XML(xml)
        self.buildFromXMLElement(xml_root)
    
    def buildFromXMLElement(self, xml_root):
        if (not xml_root.find('index') is None):
            self.index = xml_root.find('index').text
        if (not xml_root.find('text') is None):    
            self.text = xml_root.find('text').text
        if (not xml_root.find('subtitle') is None):  
            self.subtitle = xml_root.find('subtitle').text
        if (not xml_root.find('vote_total') is None):  
            self.vote_total = xml_root.find('vote_total').text
        
        votesElement = xml_root.find('votes')
        if (not votesElement is None):
            self.votes = []
            for voteElement in votesElement.findall('vote'):
                self.votes.append(Vote(xml_elemnt=voteElement))
                
        if (not xml_root.find('percentage') is None):  
            self.percentage = xml_root.find('percentage').text
        