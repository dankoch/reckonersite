'''
Created on Oct 1, 2011
@author: danko
'''
import mimetypes
import re
import logging
import urllib2

from BeautifulSoup import BeautifulSoup, Comment
from django.conf import settings
from django.template.defaultfilters import slugify
from tidylib import tidy_document
from urlparse import urljoin

logger = logging.getLogger(settings.STANDARD_LOGGER)

def purgeHtml(value):
    if (value is not None):
        return sanitizeHtml(value, "")
    
    return None

def sanitizeBioHtml(value):
    if (value is not None):
        document = sanitizeHtml(value, 'p i em strong b u a pre br ol ul li')
        document = tidyTextInput(document)
        return document
    return None

def sanitizeCommentHtml(value):
    if (value is not None):
        document = sanitizeHtml(value, 'p i em strong b u a pre br ol ul li')
        document = tidyTextInput(document)
        return document
    return None

def sanitizeDescriptionHtml(value):
    if (value is not None):
        document = sanitizeHtml(value, 'p i em strong b u a pre br ol ul li img')
        document = tidyTextInput(document)
        return document
    return None

def sanitizeHtml(value, valid_tags, base_url=None):
    rjs = r'[\s]*(&#x.{1,7})?'.join(list('javascript:'))
    rvb = r'[\s]*(&#x.{1,7})?'.join(list('vbscript:'))
    re_scripts = re.compile('(%s)|(%s)' % (rjs, rvb), re.IGNORECASE)
    validTags = valid_tags.split()
    validAttrs = 'href src width height'.split()
    urlAttrs = 'href src'.split() # Attributes which should have a URL
    soup = BeautifulSoup(value)
    for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
        # Get rid of comments
        comment.extract()
    for tag in soup.findAll(True):
        if tag.name not in validTags:
            tag.hidden = True
        attrs = tag.attrs
        tag.attrs = []
        for attr, val in attrs:
            if attr in validAttrs:
                val = re_scripts.sub('', val) # Remove scripts (vbs & js)
                if attr in urlAttrs:
                    val = urljoin(base_url, val) # Calculate the absolute url
                tag.attrs.append((attr, val))

    return soup.renderContents().decode('utf8')


def slugifyTitle(value):
    slugifiedTitle = None;
    
    if (value):
        slugifiedTitle = slugify(value)
        if (len(slugifiedTitle) > 80):
            slugifiedTitle = slugifiedTitle[0:79]
            
    return slugifiedTitle


def tidyTextInput(document):
    tidy_doc, errors = tidy_document(document, options={'show-body-only' : 1})
    return tidy_doc


def verifyUrl(url):
    '''Verifies that a specified URL exists and can be opened'''
    try:
        handle = urllib2.urlopen(url, None, timeout=10)
        handle.close()
    except:
        logger.warn("Url not found during verification: " + url)
        return False

    return True

def getUrlMimeType(url):
    '''Determines the MIME Type associated with a URL'''
    try:
        return mimetypes.guess_type(url, False)[0]
    except:
        logger.warn("Error when determining the MIME type for url: " + url)
    
    return None

def getUrlDownloadSize(url):
    '''Determines the size of a file at the specified URL'''
    try:
        site = urllib2.urlopen(url)
        meta = site.info()
        return meta.getheaders("Content-Length")[0]
    except:
        logger.warn("Unable to get size for object at url: " + url)
        
    return None