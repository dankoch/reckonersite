'''
Created on Oct 16, 2011

@author: danko
'''
import datetime
import traceback

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

from reckonersite.util.dateutil import getTimeDelta, getCurrentDateTime, timeDeltaFormatter, convertDateTimeToForm

register = template.Library()

@register.filter
def condense_int(value):
    '''
    Converts a positive integer or string into a condensed string value.  
    Compressions are as follows:
    
      x < 1,000:  Converts to 'xxx'
      1,000 <= x < 100,000:  Converts to 'x.xK' or 'xx.xK'
      100,000 <= x < 1,000,000: Converts to 'xxxK'
      1,000,000 <= x < 100,000,000: Converts to 'x.xM' or 'xx.xM'
    '''
    if (value):
        int_value = int(value)
        
        if (int_value < 1000):
            return value
        elif (int_value < 100000):
            k_value = int_value / 1000
            dec_value = (int_value % 1000) / 100
            return str(k_value) + "." + str(dec_value) + "K"
        elif (int_value < 1000000):
            k_value = int_value / 1000
            return str(k_value) + "K"
        elif (int_value < 100000000):
            m_value = int_value / 1000000
            dec_value = (int_value % 1000000) / 100000
            return str(m_value) + "." + str(dec_value) + "M"
        elif (int_value < 1000000000):
            m_value = int_value / 1000000
            return str(m_value) + "M"
        
    return "0"
condense_int.is_safe = True

@register.filter
def time_since(value):
    '''
    Creates a display string to show the time since the specified date.
    '''
    if (value):
        timeDelta = getTimeDelta(value, getCurrentDateTime())
        
        return timeDeltaFormatter(timeDelta)
        
    return ""
time_since.is_safe = True

@register.filter
def until_time(value):
    '''
    Creates a display string to show the time until the specified date.
    '''
    if (value):
        timeDelta = getTimeDelta(getCurrentDateTime(), value)
        
        return timeDeltaFormatter(timeDelta)
        
    return ""
until_time.is_safe = True

@register.filter
def form_time(value):
    '''
    Creates a display string to show a date used in a form.
    '''
    
    if (isinstance(value, datetime.datetime)):
        return convertDateTimeToForm(value)

    return ""
form_time.is_safe = True

@register.filter
def get_user_name(value):
    '''
    Accepts an object of type reckonersite.domain.reckonuser or reckonersite.domain.sitecustomuser
    and uses it to retrieve the raw name string according to how the user wants to display it.
    '''
    returnString=""
    
    try:        
        if (value.use_username):
            returnString= value.username 
        else:
            returnString= "".join((value.first_name, " ", value.last_name,))    
    finally:
        return mark_safe(returnString)

@register.filter
def print_user_name(value):
    '''
    Accepts an object of type reckonersite.domain.reckonuser or reckonersite.domain.sitecustomuser
    and uses it to print out the standard user display name.
    '''
    returnString=""
    
    try:        
        if (value.use_username):
            returnString= "".join(("<a href=\"", value.getURL(), "\">",
                                       value.username,
                                       "</a>"))  
        else:
            returnString= "".join(("<a href=\"", value.getURL(), "\">",
                                       value.first_name, " ", value.last_name,
                                       "</a>"))    
    finally:
        return mark_safe(returnString)
    
@register.filter
def print_tag_link(value):
    '''
    Accepts an object of type reckonersite.domain.reckoning.Tag and converts it 
    into a link to the 'display posts tagged by this' screen.
    '''
    returnString=""
    
    try:
        returnString= "".join(("<a href=\"", value.getURL(), "\">",
                                   value.tag,
                                   "</a>"))
    finally:
        return mark_safe(returnString)
    
@register.filter
def print_podcast_link(value):
    '''
    Accepts a url and automatically adds the Podcast tracking prefix.
    '''
    returnString=value

    try:
        # Add in tracking prefix to URL by splitting off the http prefix and adding the prefix string.
        url_seq = value.split("//", 1)
        if (len(url_seq) == 2):
            returnString = "".join((settings.PODCAST_TRACKING_PREFIX, url_seq[1],))
        else:
            returnString = "".join((settings.PODCAST_TRACKING_PREFIX, url_seq[0],))
    finally:
        return mark_safe(returnString)