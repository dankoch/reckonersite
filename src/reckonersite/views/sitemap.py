'''
Created on Nov 16, 2011
@author: danko
'''
import gzip
import logging
import traceback

from django.conf import settings
from django.http import HttpResponseRedirect

from reckonersite.client.authclient import client_get_user_summaries
from reckonersite.client.contentclient import client_get_contents
from reckonersite.client.reckoningclient import client_get_closed_reckonings, client_get_open_reckonings
from reckonersite.domain.sitemap import SiteMap
from reckonersite.domain.sitemapdoc import SiteMapDoc
from reckonersite.domain.sitemapindex import SiteMapIndex
from reckonersite.domain.sitemapurl import SiteMapUrl
from reckonersite.util.dateutil import getCurrentDateTimeXmlString

logger = logging.getLogger(settings.STANDARD_LOGGER)  

def writeSiteMaps(request):
    '''
    Calls necessary functions to create the sitemap files.
    '''
    
    # Important KLUDGE NOTE:
    # The getCurrentDateTimeString function returns local time, but we're artificially marking everything as
    # UTC via the XML string (using the 'Z' suffix).  Why?  Because for what we're using the date for, it's mostly
    # harmless to do this, and a heck of a lot easier than futzing with pytz to get the time zones correct.
    #
    # BEWARE IN THE FUTURE.
    
    
    if request.user.has_perm('SITEMAP'):
        try:
            siteMapDocs = []
            
            # Open Reckonings
            f = gzip.open(settings.XML_SITEMAP_FILE_LOCATION + '/sitemap_open_reckonings.xml.gz', 'wb')
            f.write(createOpenReckoningSitemap(request).getXMLString())
            f.close()
            
            siteMapDocs.append(SiteMapDoc(loc=settings.XML_SITEMAP_ROOT_URL + '/sitemap_open_reckonings.xml.gz',
                                          lastmod="".join((getCurrentDateTimeXmlString(), "Z"))))
            
            # Closed Reckonings
            f = gzip.open(settings.XML_SITEMAP_FILE_LOCATION + '/sitemap_closed_reckonings.xml.gz', 'wb')
            f.write(createClosedReckoningSitemap(request).getXMLString())
            f.close()
            
            siteMapDocs.append(SiteMapDoc(loc=settings.XML_SITEMAP_ROOT_URL + '/sitemap_closed_reckonings.xml.gz',
                                          lastmod="".join((getCurrentDateTimeXmlString(), "Z"))))
            
            # Contents
            f = gzip.open(settings.XML_SITEMAP_FILE_LOCATION + '/sitemap_contents.xml.gz', 'wb')
            f.write(createContentsSitemap(request).getXMLString())
            f.close()
            
            siteMapDocs.append(SiteMapDoc(loc=settings.XML_SITEMAP_ROOT_URL + '/sitemap_contents.xml.gz',
                                          lastmod="".join((getCurrentDateTimeXmlString(), "Z"))))
            
            # User Profiles
            f = gzip.open(settings.XML_SITEMAP_FILE_LOCATION + '/sitemap_profiles.xml.gz', 'wb')
            f.write(createUsersSitemap(request).getXMLString())
            f.close()
            
            siteMapDocs.append(SiteMapDoc(loc=settings.XML_SITEMAP_ROOT_URL + '/sitemap_profiles.xml.gz',
                                          lastmod="".join((getCurrentDateTimeXmlString(), "Z"))))
            
            # Site Pages
            f = gzip.open(settings.XML_SITEMAP_FILE_LOCATION + '/sitemap_sites.xml.gz', 'wb')
            f.write(createSitePagesSitemap(request).getXMLString())
            f.close()
            
            siteMapDocs.append(SiteMapDoc(loc=settings.XML_SITEMAP_ROOT_URL + '/sitemap_sites.xml.gz',
                                          lastmod="".join((getCurrentDateTimeXmlString(), "Z"))))
            
            # Index Page
            siteMapIndex = SiteMapIndex(sitemaps=siteMapDocs)
            f = open(settings.XML_SITEMAP_FILE_LOCATION + '/sitemap.xml', 'wb')
            f.write(siteMapIndex.getXMLString())
            f.close()
            
        except Exception:
            logger.error("Exception when showing contact us page:") 
            logger.error(traceback.print_exc(8))
            raise Exception     
        
    return HttpResponseRedirect('/')           

def createOpenReckoningSitemap(request):
    '''
    Function responsible for returning Open Reckoning URLs to be included in The Reckoner sitemap, as
    used for search engine traversal.
    
    Return value is a mutable list of SiteMapUrl objects.
    '''    
    siteMapUrlList = []
        
    # Open Reckonings
    open_reckonings_response = client_get_open_reckonings(sort_by="postingDate", ascending=False,
                                                          session_id=request.user.session_id)
    
    if (open_reckonings_response.status.success):
        for reckoning in open_reckonings_response.reckonings:
            siteMapUrlList.append(SiteMapUrl(loc="".join((settings.SITE_ROOT,reckoning.getURL(),)), 
                                             changefreq='hourly',
                                             priority='0.7')) 
            
    return SiteMap(urls = siteMapUrlList) 
            
def createClosedReckoningSitemap(request):
    '''
    Function responsible for returning Closed Reckoning URLs to be included in The Reckoner sitemap, as
    used for search engine traversal.
    
    Return value is a SiteMap object.
    '''    
    siteMapUrlList = []
        
    # Closed Reckonings
    closed_reckonings_response = client_get_closed_reckonings(sort_by="postingDate", ascending=False, size=50000,
                                                          session_id=request.user.session_id)
    
    if (closed_reckonings_response.status.success):
        for reckoning in closed_reckonings_response.reckonings:
            siteMapUrlList.append(SiteMapUrl(loc="".join((settings.SITE_ROOT,reckoning.getURL(),)), 
                                             changefreq='monthly',
                                             priority='0.6'))
            
    return SiteMap(urls = siteMapUrlList)
            
def createContentsSitemap(request):
    '''
    Function responsible for returning Content URLs to be included in The Reckoner sitemap, as
    used for search engine traversal.
    
    Return value is a SiteMap object.
    '''    
    siteMapUrlList = []
        
    # Contents
    contents_response = client_get_contents(sort_by="postingDate", ascending=False,
                                                          session_id=request.user.session_id)
    
    if (contents_response.status.success):
        for content in contents_response.contents:
            siteMapUrlList.append(SiteMapUrl(loc="".join((settings.SITE_ROOT,content.getURL(),)), 
                                             changefreq='monthly',
                                             priority='0.6'))  
            
    return SiteMap(urls = siteMapUrlList)

def createUsersSitemap(request):
    '''
    Function responsible for returning Users URLs to be included in The Reckoner sitemap, as
    used for search engine traversal.
    
    Return value is a SiteMap object.
    '''    
    siteMapUrlList = []
        
    # User Profiles
    user_response = client_get_user_summaries(sort_by="firstLogin", ascending=False, size=50000,
                                                          session_id=request.user.session_id)
    
    if (user_response.status.success):
        for user in user_response.reckoner_user_summaries:
            siteMapUrlList.append(SiteMapUrl(loc="".join((settings.SITE_ROOT,user.getURL(),)), 
                                             changefreq='monthly',
                                             priority='0.6'))   
            
    return SiteMap(urls = siteMapUrlList)     
              

def createSitePagesSitemap(request):
    '''
    Function responsible for returning static URLs to be included in The Reckoner sitemap, as
    used for search engine traversal.
    
    Return value is a SiteMap object.
    
    NOTE: For static pages, these values need to be kept synchronized with the Django URLs list.
    '''
    siteMapUrlList = []
    
    # Home Page
    siteMapUrlList.append(SiteMapUrl(loc="".join((settings.SITE_ROOT,)), 
                                     lastmod="".join((getCurrentDateTimeXmlString(), "Z")),
                                     changefreq='always',
                                     priority='0.8'))
    
    # Blog Home Page
    siteMapUrlList.append(SiteMapUrl(loc="".join((settings.SITE_ROOT,"/blog",)), 
                                     lastmod="".join((getCurrentDateTimeXmlString(), "Z")),
                                     changefreq='always',
                                     priority='0.8'))
    
    # Search
    siteMapUrlList.append(SiteMapUrl(loc="".join((settings.SITE_ROOT,"/search",)), 
                                     changefreq='yearly'))
    
    # About
    siteMapUrlList.append(SiteMapUrl(loc="".join((settings.SITE_ROOT,"/about",)), 
                                     changefreq='monthly',
                                     priority='0.7'))
    
    # Contact Us
    siteMapUrlList.append(SiteMapUrl(loc="".join((settings.SITE_ROOT,"/contact-us",)), 
                                     changefreq='yearly'))
    
    # Privacy Policy
    siteMapUrlList.append(SiteMapUrl(loc="".join((settings.SITE_ROOT,"/privacy-policy",)), 
                                     changefreq='monthly',
                                     priority='0.3'))
    
    # Open Reckonings Page
    siteMapUrlList.append(SiteMapUrl(loc="".join((settings.SITE_ROOT,"/open-reckonings",)), 
                                     lastmod="".join((getCurrentDateTimeXmlString(), "Z")),
                                     changefreq='always',
                                     priority='0.6'))    
    
    # Closed Reckonings Page
    siteMapUrlList.append(SiteMapUrl(loc="".join((settings.SITE_ROOT,"/closed-reckonings",)), 
                                     lastmod="".join((getCurrentDateTimeXmlString(), "Z")),
                                     changefreq='always',
                                     priority='0.6'))  
    
    # Post Reckonings Page
    siteMapUrlList.append(SiteMapUrl(loc="".join((settings.SITE_ROOT,"/post-reckoning-welcome",)), 
                                     changefreq='monthly',
                                     priority='0.5'))
        
    return SiteMap(urls = siteMapUrlList)
