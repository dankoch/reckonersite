'''
Created on Oct 1, 2011
@author: danko
'''
import logging
from django.conf import settings

logger = logging.getLogger(settings.STANDARD_LOGGER)

def pageDisplay(current_page, page_size, total_items):
    '''
    Responsible for determining how the page selector elements on a multi-page screen should
    be displayed.
    
    Accepts the page currently displayed, the number of items per page (page_size), and the total number
    of items to page across (total_items)
    
    Returns a dictionary with three possible elements along with the last page:
    
    begin-pages         page-spread             end-pages
     1...               5,6,7,8,9               ...32
    '''
    
    # Spread of pages around the current page.  Should always be odd.
    spread = 5
    
    # Determine the last page.
    final_page = int(total_items) / int(page_size)
    if (int(total_items) % int(page_size)):
        final_page += 1
    
    begin_pages = None
    page_spread = None
    end_pages = None
    
    if (spread < final_page):
        if ((int(current_page) - spread / 2) <= 1):
            begin_pages = range(1,spread+1)
        else:
            begin_pages = range(1,2)
        
        if (((int(current_page) - spread / 2) > 1) and ((int(current_page) + spread / 2) < final_page)):
            page_spread = range(int(current_page) - spread/2, int(current_page) + spread/2+1)
            
        if ((int(current_page) + spread / 2) >= final_page):
            end_pages = range((final_page - spread) + 1,final_page+1)
        else:
            end_pages = range(final_page, final_page+1)
    else:
        begin_pages = range(1, final_page+1)             
    
    return ({'begin_pages' : begin_pages,
             'page_spread' : page_spread,
             'end_pages' : end_pages,
             'final_page' : final_page})