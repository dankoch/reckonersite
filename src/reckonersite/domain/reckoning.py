'''
Created on Aug 23, 2011
@author: danko
'''
from xml.etree import cElementTree as cET
from reckonersite.domain.answer import Answer
from reckonersite.domain.base import Base, buildXml
from reckonersite.domain.comment import Comment
from reckonersite.domain.vote import Vote

class Reckoning(Base):
    '''Object definition of a basic reckoning.  Maintained to be synchronized with the Reckoner API'''

    def __init__(self, id=None, question=None, description=None, answers=None,
                 submitter_id=None, approver_id=None, approved=False, rejected=False,
                 open=False, anonymous_requested=False, anonymous=False, submission_date=None,
                 posting_date=None, closing_date=None, interval=None, comments=None, comment_index=None,
                 flags=None, favorites=None, tags=None, highlighted=False):
        
        self.id = id
        self.question = question
        self.description = description
        self.answers = answers
        self.submitter_id = submitter_id
        self.approver_id = approver_id
        self.approved = approved
        self.rejected = rejected
        self.open = open
        self.anonymous_requested = anonymous_requested
        self.anonymous = anonymous
        self.submission_date = submission_date
        self.posting_date = posting_date
        self.closing_date = closing_date
        self.interval = interval
        self.comments = comments
        self.comment_index = comment_index
        self.flags = flags
        self.favorites = favorites
        self.tags = tags
        self.highlighted = highlighted
        
    def getXML(self):
        return (buildXml(self.__dict__, 'reckoning'))
    
    def getXMLString(self):
        print cET.tostring(self.getXML())
        return cET.tostring(self.getXML())
    
    def getPostingXML(self, user_token):
        posting = cET.Element('reckoning_post')
        posting.append(self.getXML())
        
        token = cET.SubElement(posting, 'user_token')
        token.text = user_token
        
        return posting
    
    def getPostingXMLString(self, user_token):
        return cET.tostring(self.getPostingXML(user_token))   
            
        
        