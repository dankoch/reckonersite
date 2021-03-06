'''
Created on Aug 23, 2011
@author: danko
'''
from urllib import quote_plus

from datetime import datetime
from xml.etree import cElementTree as cET
from reckonersite.domain.answer import Answer
from reckonersite.domain.base import Base, buildXml, convertToDateTime
from reckonersite.domain.comment import Comment
from reckonersite.domain.favorite import Favorite
from reckonersite.domain.flag import Flag
from reckonersite.domain.media import Media
from reckonersite.domain.reckoneruser import ReckonerUser
from reckonersite.util.validation import slugifyTitle

class Reckoning(Base):
    '''Object definition of a basic reckoning.  Maintained to be synchronized with the Reckoner API'''

    def __init__(self, id=None, question=None, description=None, answers=None,
                 submitter_id=None, approver_id=None, approved=None, rejected=None,
                 open=None, anonymous_requested=None, anonymous=None, submission_date=None,
                 posting_date=None, closing_date=None, interval=None, comments=None, comment_index=None,
                 media_items=None,
                 commentary=None, commentary_user_id=None, commentary_user=None, posting_user=None,
                 flags=None, favorites=None, tags=None, highlighted=None, views=None, 
                 tag_csv=None,
                 xml_string=None, xml_element=None):
        
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
        self.media_items = media_items
        self.commentary = commentary
        self.commentary_user_id = commentary_user_id
        self.commentary_user = commentary_user
        self.posting_user = posting_user
        self.flags = flags
        self.favorites = favorites
        self.tags = tags
        self.highlighted = highlighted
        self.views = views
        
        if not tag_csv is None:
            self.setTagsFromCSV(tag_csv)
        
        if not xml_string is None:
            self.buildFromXMLString(xml_string)
            
        if not xml_element is None:
            self.buildFromXMLElement(xml_element)
            
        self.url = self.getURL()
        self.results_url = self.getResultsURL()
        self.total_votes = self.getTotalVotes()
        
    def getXML(self):
        return (buildXml(self.__dict__, 'reckoning'))
    
    def getXMLString(self):
        return cET.tostring(self.getXML())
    
    def getPostingXML(self, session_id):
        posting = cET.Element('reckoning_post')
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
            
        if (not xml_root.find('commentary') is None):
            self.commentary = xml_root.find('commentary').text
        if (not xml_root.find('commentary_user_id') is None):
            self.commentary_user_id = xml_root.find('commentary_user_id').text
        if (not xml_root.find('commentary_user') is None):
            self.commentary_user=ReckonerUser(xml_element = xml_root.find('commentary_user'))

        if (not xml_root.find('posting_user') is None):
            self.posting_user=ReckonerUser(xml_element = xml_root.find('posting_user'))

        commentsElement = xml_root.find('comments')
        if (not commentsElement is None):
            self.comments=[]
            for commentElement in commentsElement.findall('comment'):
                self.comments.append(Comment(xml_element=commentElement))
                
        mediaItemsElement = xml_root.find('media_items')
        if (not mediaItemsElement is None):
            self.media_items=[]
            for mediaElement in mediaItemsElement.findall('media'):
                self.media_items.append(Media(xml_element=mediaElement))
           
        flagsElement = xml_root.find('flags')        
        if (not flagsElement is None):
            self.flags=[]
            for flagElement in flagsElement.findall('flag'):
                self.flags.append(Flag(xml_element=flagElement))
        
        favoritesElement = xml_root.find('favorites')
        if (not favoritesElement is None):               
            self.favorites=[]
            for favoriteElement in favoritesElement.findall('favorite'):
                self.favorites.append(Favorite(xml_element=favoriteElement))
        
        tagsElement = xml_root.find('tags')
        if (not tagsElement is None):    
            tags=[]
            for tagElement in tagsElement.findall('tag'):
                tags.append(tagElement.text)
                self.tags = self.buildTagList(tags)

        if (not xml_root.find('highlighted') is None):           
            self.highlighted = (xml_root.find('highlighted').text == 'true')
            
        if (not xml_root.find('views') is None):
            self.views = xml_root.find('views').text
    
    def getTagCSV(self):
        csv=""
        if (self.tags):
            for tag in self.tags:
                csv += tag.tag + ","
        
        if (len(csv) > 0):
            return csv[:-1]
        
        return csv
    
    def setTagsFromCSV(self, csv):
        tags = csv.split(",")
        
        self.tags = self.buildTagList(tags)
        
    def buildTagList(self, tags):
        tagList = []
        for tag in tags:
            if (tag and not tag == ""):
                tagList.append(Tag(tag.strip()))
        
        return tagList
    
    def getTotalVotes(self):
        if (self.answers):
            totalVotes = 0
            for answer in self.answers:
                if (answer.vote_total):
                    totalVotes += int(answer.vote_total)
    
            return totalVotes
        return None
    
    def getURL(self):
        if (self.id and self.question):
            return '/reckoning/' + self.id + "/" + slugifyTitle(self.question)
        
        return None
    
    def getResultsURL(self):
        if (self.id and self.question):
            return '/reckoning/results/' + self.id + "/" + slugifyTitle(self.question)
        
        return None
    
    def getLeadingAnswer(self):
        '''
        Gets the index of the answer with the most votes.
        A '-1' value connotes a tie or an error.
        '''
        index=-1
        highVal=0
        
        for answer in self.answers:
            if (answer.vote_total):
                if (int(answer.vote_total) > highVal):
                    highVal = int(answer.vote_total)
                    index = answer.index
                elif (int(answer.vote_total) == highVal):
                    index = -1

        return index
        
class Tag(Base):
    def __init__(self, tag=None):
        self.tag = tag
        
    def getXML(self):
        return (buildXml(self.tag, 'tag'))
    
    def getXMLString(self):
        return cET.tostring(self.getXML())        
    
    def getURL(self):
        if (self.tag):
            return '/reckonings/tag/' + quote_plus(self.tag)