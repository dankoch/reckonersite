'''
Created on Oct 16, 2011

@author: danko
'''
import datetime

from django import template
from django.utils.safestring import mark_safe

from reckonersite.util.dateutil import getTimeDelta, getCurrentDateTime, timeDeltaFormatter

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
def print_user_name(value):
    '''
    Accepts an object of type reckonersite.domain.reckonuser and uses it to
    print out the standard user display name.
    '''
    returnString=""
    
    try:
        returnString= "".join(("<a href=\"", value.getURL(), "\">",
                                   value.first_name, " ", value.last_name,
                                   "</a>"))
    finally:
        return mark_safe(returnString)