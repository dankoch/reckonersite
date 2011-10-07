'''
Created on Oct 1, 2011
@author: danko
'''
import datetime

def getRemainingTime(closingDate):
    remainingTime={}
    if (closingDate):
        timeDelta = getTimeDelta(getCurrentDateTime(), closingDate)
        
        remainingTime['days'] = timeDelta.days
        remainingTime['hours'], remainder = divmod(timeDelta.seconds, 3600)
        remainingTime['minutes'], remainingTime['seconds'] = divmod(remainder, 60)
            
    return remainingTime

def getTimeDelta(startDate, endDate):
    return (endDate - startDate)

def getCurrentDateTime():
    return datetime.datetime.now()

