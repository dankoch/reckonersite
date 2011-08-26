'''
Created on Aug 23, 2011
@author: danko
'''
from xml.etree import cElementTree as cET
from reckonersite.domain.base import Base, buildXml

class Vote(Base):
    '''Object definition of a single vote (as commonly attached to an Answer attached to a Reckoning)
       This object should be kept synchronized with the Reckoner API'''

    def __init__(self, voter_id=None, answer_index=None, voting_date=None, anonymous=None, ip=None,
                 user_agent=None, latitude=None, longitude=None):
        
        self.voter_id=voter_id
        self.answer_index=answer_index
        self.voting_date=voting_date
        self.anonymous=anonymous
        self.ip=ip
        self.user_agent=user_agent
        self.latitude=latitude
        self.longitude=longitude
    
    def getXML(self):
        return (buildXml(self.__dict__, 'vote'))
    
    def getXMLString(self):
        return cET.tostring(self.getXML())