'''
Created on Oct 1, 2011
@author: danko
'''
import re
import logging

from BeautifulSoup import BeautifulSoup, Comment
from django.conf import settings
from django.template.defaultfilters import slugify
from tidylib import tidy_document
from urlparse import urljoin

logger = logging.getLogger(settings.STANDARD_LOGGER)

def purgeHtml(value):
    return sanitizeHtml(value, "")

def sanitizeBioHtml(value):
    document = sanitizeHtml(value, 'p i em strong b u a pre br ol ul li')
    document = tidyTextInput(document)
    return document

def sanitizeCommentHtml(value):
    document = sanitizeHtml(value, 'p i em strong b u a pre br ol ul li')
    document = tidyTextInput(document)
    return document

def sanitizeDescriptionHtml(value):
    document = sanitizeHtml(value, 'p i em strong b u a pre br ol ul li img')
    document = tidyTextInput(document)
    return document

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