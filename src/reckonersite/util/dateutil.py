'''
Created on Oct 1, 2011
@author: danko
'''
from datetime import datetime

def convertXmlToDateTime(string_val):
    if (string_val):
        time = datetime.strptime(string_val[0:18], "%Y-%m-%dT%H:%M:%S")
        return time
    
    return None

def convertDateTimeToXml(date_val):
    if (date_val):
        string = date_val.strftime("%Y-%m-%dT%H:%M:%S")
        return string
    
    return None

def convertFormToDateTime(string_val):
    if (string_val):
        time = datetime.strptime(string_val[0:16], "%m/%d/%Y %H:%M")
        return time
    
    return None

def convertDateTimeToForm(date_val):
    if (date_val):
        string = date_val.strftime("%m/%d/%Y %H:%M")
        return string
    
    return None

def getTimeDelta(startDate, endDate):
    return (endDate - startDate)

def getCurrentDateTime():
    return datetime.now()

def getCurrentDateTimeXmlString():
    return convertDateTimeToXml(datetime.now())

def timeDeltaFormatter(timeDelta):
    returnString = ""
    
    if (timeDelta):
        remainingTime = {}
        
        remainingTime['days'] = timeDelta.days
        remainingTime['hours'], remainder = divmod(timeDelta.seconds, 3600)
        remainingTime['minutes'], remainingTime['seconds'] = divmod(remainder, 60)
        
        if (remainingTime['days']):
            returnString += str(remainingTime['days'])
            if (remainingTime['days'] > 1):
                returnString += " days "
            else:
                returnString += " day "
        
        if (remainingTime['hours']):
            returnString += str(remainingTime['hours'])
            if (remainingTime['hours'] > 1):
                returnString += " hours "
            else:
                returnString += " hour "
        
        returnString += str(remainingTime['minutes'])
        if (remainingTime['minutes'] > 1):
            returnString += " minutes"
        else:
            returnString += " minute"

    return returnString