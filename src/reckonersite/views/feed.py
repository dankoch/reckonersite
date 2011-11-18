'''
Created on Nov 17, 2011

@author: danko
'''

import logging
import sys
import traceback

from django.conf import settings
from django.http import HttpResponse
from django.utils.feedgenerator import Rss201rev2Feed

from reckonersite.client.contentclient import client_get_contents
from reckonersite.client.reckoningclient import client_get_open_reckonings, \
                                                client_get_closed_reckonings

logger = logging.getLogger(settings.STANDARD_LOGGER)  

def latest_open_reckonings_feed(request):
    try:
        syndicationFeed = Rss201rev2Feed(title = "The Reckoner! Open Reckonings Feed!",
                                         link = "".join((settings.SITE_ROOT,"/open-reckonings",)),
                                         description = "The newest open reckonings posted to The Reckoner! Check 'em out!",
                                         subtitle = "The newest open reckonings posted to The Reckoner! Check 'em out!",
                                         feed_url = "".join((settings.SITE_ROOT,"/feed/open-reckonings",)))
        
        reckoning_response = client_get_open_reckonings(sort_by="postingDate", ascending=False,
                                                            page=0, size=15,
                                                            session_id=request.user.session_id)
        
        if (reckoning_response.status.success):
            if (reckoning_response.reckonings):
                for reckoning in reckoning_response.reckonings:
                    syndicationFeed.add_item(title=reckoning.question,
                                             link="".join((settings.SITE_ROOT,reckoning.getURL(),)),
                                             description=reckoning.description,
                                             pubdate=reckoning.posting_date,
                                             author_name="The Reckoner!",
                                             author_link=settings.SITE_ROOT)
                
                return HttpResponse(syndicationFeed.writeString("utf-8"),  mimetype="text/xml")
        else:
            logger.error("Error from getting Open Reckonings rss feed: " + reckoning_response.status.message)
    
    except Exception:      
        logger.error("Exception when showing and processing Open Reckoning RSS Feed:") 
        logger.error(traceback.print_exc(8))
        raise Exception      

    return HttpResponse("",  mimetype="text/xml")


def latest_closed_reckonings_feed(request):
    try:
        syndicationFeed = Rss201rev2Feed(title = "The Reckoner! Finished Reckonings Feed!",
                                         link = "".join((settings.SITE_ROOT,"/finished-reckonings",)),
                                         description = "The freshest finished reckonings on The Reckoner! Check out the results!",
                                         subtitle = "The freshest finished reckonings on The Reckoner! Check out the results!",
                                         feed_url = "".join((settings.SITE_ROOT,"/feed/finished-reckonings",)))
        
        reckoning_response = client_get_closed_reckonings(sort_by="closingDate", ascending=False,
                                                            page=0, size=15,
                                                            session_id=request.user.session_id)
        
        if (reckoning_response.status.success):
            if (reckoning_response.reckonings):
                for reckoning in reckoning_response.reckonings:
                    syndicationFeed.add_item(title=reckoning.question,
                                             link="".join((settings.SITE_ROOT,reckoning.getURL(),)),
                                             description=reckoning.description,
                                             pubdate=reckoning.closing_date,
                                             author_name="The Reckoner!",
                                             author_link=settings.SITE_ROOT)
                
                return HttpResponse(syndicationFeed.writeString("utf-8"),  mimetype="text/xml")
        else:
            logger.error("Error from getting Closed Reckonings RSS feed: " + reckoning_response.status.message)
    
    except Exception:      
        logger.error("Exception when showing and processing Closed Reckoning RSS Feed:") 
        logger.error(traceback.print_exc(8))
        raise Exception      

    return HttpResponse("",  mimetype="text/xml")

def latest_contents_feed(request):
    try:
        syndicationFeed = Rss201rev2Feed(title = "The Reckoner! Blog Feed!",
                                         link = "".join((settings.SITE_ROOT,"/blog",)),
                                         description = "The freshest blog content on the Reckon Blog!",
                                         subtitle = "The freshest blog content on the Reckon Blog!",
                                         feed_url = "".join((settings.SITE_ROOT,"/feed/blog",)))
        
        contents_response = client_get_contents(sort_by="postingDate", ascending=False,
                                                page=0, size=5)
        
        if (contents_response.status.success):
            if (contents_response.contents):
                for content in contents_response.contents:
                    syndicationFeed.add_item(title=content.title,
                                             link="".join((settings.SITE_ROOT,content.getURL(),)),
                                             description=content.body,
                                             pubdate=content.posting_date,
                                             author_name="The Reckoner!",
                                             author_link=settings.SITE_ROOT)
                
                return HttpResponse(syndicationFeed.writeString("utf-8"),  mimetype="text/xml")
        else:
            logger.error("Error from getting Blog RSS feed: " + contents_response.status.message)
    
    except Exception:      
        logger.error("Exception when showing and processing Blog RSS Feed:") 
        logger.error(traceback.print_exc(8))
        raise Exception      

    return HttpResponse("",  mimetype="text/xml")
