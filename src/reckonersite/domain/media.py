'''
Created on Dec 22, 2011
@author: danko
'''
from django.conf import settings
from urllib import quote_plus, unquote_plus
from xml.etree import cElementTree as cET

from reckonersite.domain.base import Base, buildXml, convertToDateTime
from reckonersite.util.validation import verifyUrl, \
                                         getUrlMimeType, \
                                         getUrlDownloadSize

class Media(Base):
    '''Object definition of a basic media item.  Maintained to be synchronized with the Reckoner API'''

    def __init__(self, media_id=None, media_type=None, name=None, small_name=None, thumbnail_name=None, full_name=None, 
                 url=None, thumbnail_url=None, full_url=None,
                 file_type=None, duration=None, size=None,
                 xml_string=None, xml_element=None):

        self.media_id = media_id
        self.media_type = media_type
        self.name = name
        self.small_name = small_name
        self.thumbnail_name = thumbnail_name
        self.full_name = full_name
        self.url = url
        self.small_name = small_name
        self.thumbnail_url = thumbnail_url
        self.full_url = full_url
        self.file_type = file_type
        self.duration = duration
        self.size = size
        
        if not xml_string is None:
            self.buildFromXMLString(xml_string)
            
        if not xml_element is None:
            self.buildFromXMLElement(xml_element)
        
    def getXML(self):
        return (buildXml(self.__dict__, 'media'))
    
    def getXMLString(self):
        return cET.tostring(self.getXML())
    
    def getPostingXML(self, session_id):
        posting = cET.Element('media_post')
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
        if (not xml_root.find('media_id') is None):
            self.media_id = xml_root.find('media_id').text
        if (not xml_root.find('media_type') is None):
            self.media_type = xml_root.find('media_type').text
        if (not xml_root.find('name') is None):
            self.name = xml_root.find('name').text
        if (not xml_root.find('small_name') is None):
            self.small_name = xml_root.find('small_name').text
        if (not xml_root.find('full_name') is None):
            self.full_name = xml_root.find('full_name').text
        if (not xml_root.find('thumbnail_name') is None):
            self.thumbnail_name = xml_root.find('thumbnail_name').text
        if (not xml_root.find('url') is None):
            self.url = xml_root.find('url').text
        if (not xml_root.find('small_url') is None):
            self.small_url = xml_root.find('small_url').text
        if (not xml_root.find('full_url') is None):
            self.full_url = xml_root.find('full_url').text
        if (not xml_root.find('thumbnail_url') is None):
            self.thumbnail_url = xml_root.find('thumbnail_url').text
        if (not xml_root.find('file_type') is None):
            self.file_type = xml_root.find('file_type').text
        if (not xml_root.find('duration') is None):
            self.duration = xml_root.find('duration').text
        if (not xml_root.find('size') is None):
            self.size = xml_root.find('size').text

def getDefaultSmallName(name):
    '''Indicates the default name for a small-size Reckoning image.'''
    if (name):
        return "".join(("small_", name))
    return None
         
def getDefaultFullName(name):
    '''Indicates the default name for a full-size Reckoning image.'''
    if (name):
        return "".join(("full_", name))
    return None
            
def getDefaultThumbnailName(name):
    '''Indicates the default name for a thumbnailed Reckoning image.'''
    if (name):
        return "".join(("thumbnail_", name))
    return None

def getDefaultUploadLocation(name=None, id=None):
    '''Indicates the default location for uploading a piece of media attached to a Reckoning.'''
    if (name and id):
        return "/".join(("reckoning", id, name))
    if (id):
        return "/".join(("reckoning", id))        
    return None
            
def getDefaultUrl(name, id):
    '''Indicates the default URL of a piece of media attached to a Reckoning.'''
    if (name and id):
        return ("".join((settings.STATIC_URL, getDefaultUploadLocation(quote_plus(name), id))))
    return None
            
def parseReckoningImageFromUploadUrl(uploadUrl):
    '''Creates a Media object based off of the supplied Reckoning Image URL.
       
       Reckoning image URLs are formatted as follows:
       <base>/reckoning/<id>/<filename>
    '''
    if (uploadUrl):
        image_media = Media()
        image_media.media_type="IMAGE"
        image_media.size = getUrlDownloadSize(uploadUrl)
        image_media.file_type = getUrlMimeType(uploadUrl)
        
        url_elements = uploadUrl.split('/')
        if (url_elements[len(url_elements) - 1]):
            image_media.name = unquote_plus(url_elements[len(url_elements) - 1])
            image_media.small_name = getDefaultSmallName(image_media.name)
            image_media.full_name = getDefaultFullName(image_media.name)
            image_media.thumbnail_name = getDefaultThumbnailName(image_media.name)
            
            url_elements[len(url_elements) - 1] = quote_plus(image_media.name)
            image_media.url = "/".join(url_elements)
            url_elements[len(url_elements) - 1] = quote_plus(image_media.small_name)
            image_media.small_url = "/".join(url_elements)
            url_elements[len(url_elements) - 1] = quote_plus(image_media.full_name)
            image_media.full_url = "/".join(url_elements)
            url_elements[len(url_elements) - 1] = quote_plus(image_media.thumbnail_name)
            image_media.thumbnail_url = "/".join(url_elements)
            
        if (url_elements[len(url_elements) - 2]):
            image_media.media_id = url_elements[len(url_elements) - 2]
        
        return image_media
        
    return None
            
        