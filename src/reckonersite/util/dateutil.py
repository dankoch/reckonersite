'''
Created on Oct 1, 2011
@author: danko
'''
import datetime

def getTimeDelta(startDate, endDate):
    return (endDate - startDate)

def getCurrentDateTime():
    return datetime.datetime.now()

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