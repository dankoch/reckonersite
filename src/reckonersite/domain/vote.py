'''
Created on Aug 23, 2011
@author: danko
'''
from datetime import datetime
from xml.etree import cElementTree as cET
from reckonersite.domain.base import Base, buildXml, convertToDateTime
from reckonersite.domain.reckoneruser import ReckonerUser

class Vote(Base):
    '''Object definition of a single vote (as commonly attached to an Answer attached to a Reckoning)
       This object should be kept synchronized with the Reckoner API'''

    def __init__(self, voter_id=None, reckoning_id=None, answer_index=None, voting_date=None, anonymous=None, ip=None,
                 user_agent=None, latitude=None, longitude=None, voting_user=None,
                 xml_string=None, xml_element=None):
        
        self.voter_id=voter_id
        self.reckoning_id=reckoning_id
        self.answer_index=answer_index
        self.voting_date=voting_date
        self.anonymous=anonymous
        self.ip=ip
        self.user_agent=user_agent
        self.latitude=latitude
        self.longitude=longitude
        self.voting_user = voting_user
        
        if not xml_string is None:
            self.buildFromXMLString(xml_string)
            
        if not xml_element is None:
            self.buildFromXMLElement(xml_element)
    
    def getXML(self):
        return (buildXml(self.__dict__, 'vote'))
    
    def getXMLString(self):
        return cET.tostring(self.getXML())
    
    def getPostingXML(self, session_id):
        posting = cET.Element('vote_post')
        posting.append(self.getXML())
        
        token = cET.SubElement(posting, 'session_id')
        token.text = session_id
        
        return posting
    
    def getPostingXMLString(self, session_id):
        return cET.tostring(self.getPostingXML(session_id))

    def buildFromXMLString(self, xml):
        xml_root = cET.XML(xml)
        self.buildFromXMLElement(xml_root)
    
    def buildFromXMLElement(self, xml_root):
        if (not xml_root.find('voter_id') is None):
            self.voter_id = xml_root.find('voter_id').text
        if (not xml_root.find('reckoning_id') is None):
            self.reckoning_id = xml_root.find('reckoning_id').text        
        if (not xml_root.find('answer_index') is None):
            self.answer_index = xml_root.find('answer_index').text
        
        if (not xml_root.find('voting_date') is None) and (not xml_root.find('voting_date').text is None):
            self.voting_date = convertToDateTime(xml_root.find('voting_date').text)
            
        if (not xml_root.find('anonymous') is None):
            self.anonymous = (xml_root.find('anonymous').text == 'true')
        if (not xml_root.find('ip') is None):
            self.ip = xml_root.find('ip').text
        if (not xml_root.find('user_agent') is None):
            self.user_agent = xml_root.find('user_agent').text
        if (not xml_root.find('latitude') is None):
            self.latitude = xml_root.find('latitude').text
        if (not xml_root.find('longitude') is None):
            self.longitude = xml_root.find('longitude').text    
            
        if (not xml_root.find('voting_user') is None):
            self.voting_user=ReckonerUser(xml_element = xml_root.find('voting_user'))