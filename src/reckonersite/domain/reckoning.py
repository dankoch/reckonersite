'''
Created on Aug 23, 2011
@author: danko
'''
from datetime import datetime
from xml.etree import cElementTree as cET
from reckonersite.domain.answer import Answer
from reckonersite.domain.base import Base, buildXml, convertToDateTime
from reckonersite.domain.comment import Comment
from reckonersite.domain.favorite import Favorite
from reckonersite.domain.flag import Flag

class Reckoning(Base):
    '''Object definition of a basic reckoning.  Maintained to be synchronized with the Reckoner API'''

    def __init__(self, id=None, question=None, description=None, answers=None,
                 submitter_id=None, approver_id=None, approved=False, rejected=False,
                 open=False, anonymous_requested=False, anonymous=False, submission_date=None,
                 posting_date=None, closing_date=None, interval=None, comments=None, comment_index=None,
                 flags=None, favorites=None, tags=None, highlighted=False, xml_string=None, xml_element=None):
        
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
        
        if not xml_string is None:
            self.buildFromXMLString(xml_string)
            
        if not xml_element is None:
            self.buildFromXMLElement(xml_element)
        
    def getXML(self):
        return (buildXml(self.__dict__, 'reckoning'))
    
    def getXMLString(self):
        return cET.tostring(self.getXML())
    
    def getPostingXML(self, user_token):
        posting = cET.Element('reckoning_post')
        posting.append(self.getXML())
        
        token = cET.SubElement(posting, 'user_token')
        token.text = user_token
        
        return posting
    
    def getPostingXMLString(self, user_token):
        return cET.tostring(self.getPostingXML(user_token))
    
    def buildFromXMLString(self, xml):
        xml_root = cET.XML(xml)
        self.buildFromXMLElement(xml_root)
    
    def buildFromXMLElement(self, xml_root):
        if (not xml_root.find('id') is None):
            self.id = xml_root.find('id').text
        if (not xml_root.find('question') is None):
            self.question = xml_root.find('question').text
        if (not xml_root.find('description') is None):
            self.description = xml_root.find('description').text
        
        answersElement = xml_root.find('answers')
        if (not answersElement is None):
            self.answers=[]
            for answerElement in answersElement.findall('answer'):
                self.answers.append(Answer(xml_element=answerElement))
        
        if (not xml_root.find('submitter_id') is None):
            self.submitter_id = xml_root.find('submitter_id').text
        if (not xml_root.find('approver_id') is None):
            self.approver_id = xml_root.find('approver_id').text
        if (not xml_root.find('approved') is None):
            self.approved = (xml_root.find('approved').text == 'true')
        if (not xml_root.find('rejected') is None):
            self.rejected = (xml_root.find('rejected').text == 'true')
        if (not xml_root.find('open') is None):
            self.open = (xml_root.find('open').text == 'true')
        if (not xml_root.find('anonymous') is None):
            self.anonymous = (xml_root.find('anonymous').text == 'true')
        if (not xml_root.find('anonymous_requested') is None):
            self.anonymous_requested = (xml_root.find('anonymous_requested').text == 'true')
        
        if (not xml_root.find('submission_date') is None) and (not xml_root.find('submission_date').text is None):
            self.submission_date = convertToDateTime(xml_root.find('submission_date').text)
        if (not xml_root.find('posting_date') is None) and (not xml_root.find('posting_date').text is None):
            self.posting_date = convertToDateTime(xml_root.find('posting_date').text)
        if (not xml_root.find('closing_date') is None) and (not xml_root.find('closing_date').text is None):
            self.closing_date = convertToDateTime(xml_root.find('closing_date').text)

        if (not xml_root.find('interval') is None):            
            self.interval = xml_root.find('interval').text
        if (not xml_root.find('comment_index') is None):
            self.comment_index = xml_root.find('comment_index').text

        commentsElement = xml_root.find('comments')
        if (not commentsElement is None):
            self.comments=[]
            for commentElement in commentsElement.findall('comment'):
                self.comments.append(Comment(xml_element=commentElement))
           
        flagsElement = xml_root.find('flags')        
        if (not flagsElement is None):
            self.flags=[]
            for flagElement in flagsElement.findall('flags'):
                self.flags.append(Flag(xml_element=flagElement))
        
        favoritesElement = xml_root.find('favorites')
        if (not favoritesElement is None):               
            self.favorites=[]
            for favoriteElement in favoritesElement.findall('favorite'):
                self.favorites.append(Favorite(xml_element=favoriteElement))
        
        tagsElement = xml_root.find('tags')
        if (not tagsElement is None):    
            self.tags=[]
            for tagElement in tagsElement.findall('tag'):
                self.tags.append(tagElement.text)

        if (not xml_root.find('highlighted') is None):           
            self.highlighted = (xml_root.find('highlighted') == 'true')  

        
        