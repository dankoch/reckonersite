'''
Created on Dec 21, 2011

@author: danko
'''

from django.utils.feedgenerator import Rss201rev2Feed

class iTunesPodcastsFeedGenerator(Rss201rev2Feed):

    def rss_attributes(self):
        return {u"version": self._version, u"xmlns:atom": u"http://www.w3.org/2005/Atom", 
                u'xmlns:itunes': u'http://www.itunes.com/dtds/podcast-1.0.dtd',
                u'xmlns:podtrac': u'http://www.podtrac.com/player2.0/tips.php#rss'}

    def add_root_elements(self, handler):
        super(iTunesPodcastsFeedGenerator, self).add_root_elements(handler)
        handler.addQuickElement(u'itunes:subtitle', self.feed['subtitle'])
        handler.addQuickElement(u'itunes:author', self.feed['author_name'])
        handler.addQuickElement(u'itunes:summary', self.feed['description'])
        handler.addQuickElement(u'itunes:category', None, {'text' : self.feed['category']})
        handler.addQuickElement(u'itunes:explicit', self.feed['itunes_explicit'])
        
        handler.startElement(u"itunes:owner", {})
        handler.addQuickElement(u'itunes:name', self.feed['itunes_name'])
        handler.addQuickElement(u'itunes:email', self.feed['itunes_email'])
        handler.endElement(u"itunes:owner")
        
        handler.addQuickElement(u'itunes:image', None, {'href' : self.feed['itunes_image_url']})
        handler.addQuickElement(u'itunes:block', self.feed['itunes_block'])
        handler.addQuickElement(u'itunes:keywords', self.feed['itunes_keywords'])
        
        handler.addQuickElement(u'podtrac:itunespodcastid', self.feed['itunes_podcast_id'])

    def add_item_elements(self,  handler, item):
        super(iTunesPodcastsFeedGenerator, self).add_item_elements(handler, item)
        handler.addQuickElement(u'itunes:subtitle', item['subtitle'])
        handler.addQuickElement(u'itunes:summary',item['summary'])
        handler.addQuickElement(u'itunes:duration',item['duration'])
        handler.addQuickElement(u'itunes:explicit',item['explicit'])
        handler.addQuickElement(u'itunes:block',item['block'])
        
        handler.addQuickElement(u'enclosure', None, {'url' : item['url'], 
                                                     'length' : item['bytes'], 
                                                     'type' : item['type']})
        
        handler.addQuickElement(u'itunes:image', None, {'href' : self.feed['itunes_image_url']})
        handler.addQuickElement(u'itunes:keywords', item['itunes_keywords'])
        handler.addQuickElement(u'podtrac:episodeimage', item['itunes_image_url'])
        handler.addQuickElement(u'guid',item['guid'])