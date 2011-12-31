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

from reckonersite.util.feed import iTunesPodcastsFeedGenerator
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

def latest_podcasts_feed(request):
    try:
        syndicationFeed = iTunesPodcastsFeedGenerator(title = settings.PODCAST_TITLE,
                                         link = "".join((settings.SITE_ROOT,)),
                                         description = settings.PODCAST_DESCRIPTION,
                                         subtitle = settings.PODCAST_SUBTITLE,
                                         feed_url = "".join((settings.SITE_ROOT,"/feed/podcast",)),
                                         author_name = settings.PODCAST_AUTHOR,
                                         category = settings.PODCAST_ITUNES_CATEGORY,
                                         itunes_explicit = settings.PODCAST_ITUNES_EXPLICIT,
                                         itunes_name = settings.PODCAST_AUTHOR_NAME,
                                         itunes_email = settings.CONTACT_US_EMAIL,
                                         itunes_image_url = settings.PODCAST_ITUNES_IMAGE,
                                         itunes_keywords = settings.PODCAST_ITUNES_KEYWORDS,
                                         itunes_podcast_id = settings.PODCAST_ITUNES_ID,
                                         itunes_block = settings.PODCAST_BLOCKED)
        
        contents_response = client_get_contents(type="PODCAST", 
                                                sort_by="postingDate", ascending=False,
                                                page=0, size=50)
        
        if (contents_response.status.success):
            if (contents_response.contents):
                for content in contents_response.contents:
                    
                    # Check to make sure media is attached to the content.
                    # If so, check for audio elements and images.  Assume the last attached is best.
                    # If no attached audio files are found, move along to the next one.
                    if (content.media_items):
                        image_url = settings.PODCAST_ITUNES_IMAGE
                        podcast = None
                        
                        for media in content.media_items:
                            if (media.media_type == "AUDIO"):
                                podcast = media
                            elif (media.media_type == "IMAGE"):
                                image_url = media.url
                        
                        if (podcast):
                            syndicationFeed.add_item(title=media.name,
                                                     link="".join((settings.SITE_ROOT,content.getURL(),)),
                                                     description=content.summary,
                                                     pubdate=content.posting_date,
                                                     subtitle=content.summary,
                                                     summary=content.summary,
                                                     duration=media.duration,
                                                     url=media.url,
                                                     type=media.file_type,
                                                     bytes=media.size,
                                                     guid=media.media_id,
                                                     block = settings.PODCAST_BLOCKED,
                                                     explicit = settings.PODCAST_ITUNES_EXPLICIT,                                                     
                                                     itunes_image_url=image_url,
                                                     itunes_keywords=content.getTagCSV())
                
                return HttpResponse(syndicationFeed.writeString("utf-8"),  mimetype="text/xml")
        else:
            logger.error("Error from getting Podcast RSS feed: " + contents_response.status.message)
    
    except Exception:      
        logger.error("Exception when showing and processing Podcast RSS Feed:") 
        logger.error(traceback.print_exc(8))
        raise Exception      

    return HttpResponse("",  mimetype="text/xml")
