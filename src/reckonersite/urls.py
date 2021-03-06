from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^post-reckoning-welcome', 'reckonersite.views.reckoning.post_reckoning_welcome'),
    (r'^post-content', 'reckonersite.views.content.post_content'),
    (r'^post-reckoning', 'reckonersite.views.reckoning.post_reckoning'),
    (r'^thanks-for-playing', 'reckonersite.views.reckoning.post_reckoning_thanks'),
    (r'^gosh-darn-it-to-heck', 'reckonersite.views.reckoning.reckoning_fail'),
    (r'^comment/content/post', 'reckonersite.views.content.post_content_comment'),    
    (r'^comment/reckoning/post', 'reckonersite.views.reckoning.post_reckoning_comment'),    
    (r'^vote/reckoning', 'reckonersite.views.reckoning.vote_reckoning'), 
    (r'^open-reckonings', 'reckonersite.views.reckoning.get_open_reckonings'),
    (r'^finished-reckonings', 'reckonersite.views.reckoning.get_closed_reckonings'),
    (r'^reckonings/tag/(?P<tag>\S+)', 'reckonersite.views.reckoning.get_tagged_reckonings'),
    (r'^random-reckoning', 'reckonersite.views.reckoning.get_random_reckoning'),
    (r'^content/(?P<id>\w+?)/(?P<title>\S+)', 'reckonersite.views.content.get_content'),
    (r'^reckoning/results/(?P<id>\w+?)/(?P<title>\S+)', 'reckonersite.views.reckoning.get_reckoning_results'), 
    (r'^reckoning/(?P<id>\w+?)/(?P<title>\S+)', 'reckonersite.views.reckoning.get_reckoning'),      
    (r'^login/tricky-ol-google', 'reckonersite.views.login.rejected_login_bad_google'),
    (r'^login/google', 'reckonersite.views.login.login_google'),
    (r'^login/facebook', 'reckonersite.views.login.login_facebook'),
    (r'^login/howdy', 'reckonersite.views.login.logged_in'),
    (r'^login/no-sweat', 'reckonersite.views.login.rejected_login'),
    (r'^login/logout', 'reckonersite.views.login.logout'),
    (r'^login/sign-up', 'reckonersite.views.login.sign_up_page'),   
    (r'^login/new-user-welcome', 'reckonersite.views.login.new_user_welcome'),       
    (r'^login', 'reckonersite.views.login.login_page'),
    (r'^blog', 'reckonersite.views.content.content_list_page', { 'content_type' : 'blog'}),
    (r'^podcast', 'reckonersite.views.content.content_list_page', { 'content_type' : 'podcast'}),
    (r'^admin/flagged', 'reckonersite.views.admin.flag_summary_page'),
    (r'^admin/user-permissions', 'reckonersite.views.admin.user_permissions_page'),
    (r'^admin/approval', 'reckonersite.views.admin.reckoning_approval_page'),
    (r'^admin', 'reckonersite.views.admin.admin_page'),
    (r'^user/(?P<id>\w+?)/(?P<name>\S+)', 'reckonersite.views.user.get_user_profile'),
    (r'^privacy-policy', 'reckonersite.views.site.privacy_policy_page'),
    (r'^contact-us/submit', 'reckonersite.views.site.submit_contact_us_page'),
    (r'^contact-us-success', 'reckonersite.views.site.contact_us_success_page'),    
    (r'^contact-us', 'reckonersite.views.site.contact_us_page'),  
    (r'^about', 'reckonersite.views.site.about_page'),   
    (r'^search', 'reckonersite.views.site.search_page'),
    (r'^generate/sitemap.xml', 'reckonersite.views.sitemap.writeSiteMaps'), 
    (r'^anonybot-3000', 'reckonersite.views.home.home_page'),
    (r'^$', 'reckonersite.views.home.home_page'),
    
    (r'^feed/open-reckonings', 'reckonersite.views.feed.latest_open_reckonings_feed'),
    (r'^feed/finished-reckonings', 'reckonersite.views.feed.latest_closed_reckonings_feed'),
    (r'^feed/blog', 'reckonersite.views.feed.latest_contents_feed'),
    (r'^feed/podcast', 'reckonersite.views.feed.latest_podcasts_feed'),
    
    (r'^404.html', direct_to_template, {'template': '404.html'}),
    (r'^500.html', direct_to_template, {'template': '500.html'}),    

    (r'^ajax/comment/content/update', 'reckonersite.views.content.update_content_comment'),
    (r'^ajax/comment/content/delete', 'reckonersite.views.content.delete_content_comment'),    
    (r'^ajax/comment/reckoning/update', 'reckonersite.views.reckoning.update_reckoning_comment'),
    (r'^ajax/comment/reckoning/delete', 'reckonersite.views.reckoning.delete_reckoning_comment'),
    (r'^ajax/notes/content/comment/flag/(?P<id>\w+)', 'reckonersite.views.note.post_content_comment_flag'),
    (r'^ajax/notes/content/flag/(?P<id>\w+)', 'reckonersite.views.note.post_content_flag'),
    (r'^ajax/notes/content/comment/favorite/(?P<id>\w+)', 'reckonersite.views.note.post_content_comment_favorite'),
    (r'^ajax/notes/content/favorite/(?P<id>\w+)', 'reckonersite.views.note.post_content_favorite'),
    (r'^ajax/notes/reckoning/comment/flag/(?P<id>\w+)', 'reckonersite.views.note.post_reckoning_comment_flag'),
    (r'^ajax/notes/reckoning/flag/(?P<id>\w+)', 'reckonersite.views.note.post_reckoning_flag'),
    (r'^ajax/notes/reckoning/comment/favorite/(?P<id>\w+)', 'reckonersite.views.note.post_reckoning_comment_favorite'),
    (r'^ajax/notes/reckoning/favorite/(?P<id>\w+)', 'reckonersite.views.note.post_reckoning_favorite'),
    (r'^ajax/content/recentblog', 'reckonersite.views.blog.get_recent_blog_ajax'),
    (r'^ajax/content/update', 'reckonersite.views.content.update_content_ajax'),
    (r'^ajax/content/reject', 'reckonersite.views.content.reject_content_ajax'),
    (r'^ajax/content/commentary/delete', 'reckonersite.views.content.delete_content_commentary'),    
    (r'^ajax/reckoning/related/(?P<id>\w+)', 'reckonersite.views.reckoning.get_related_reckonings'),  
    (r'^ajax/reckoning/top', 'reckonersite.views.reckoning.get_top_reckonings'),  
    (r'^ajax/reckoning/update', 'reckonersite.views.reckoning.update_reckoning_ajax'),
    (r'^ajax/reckoning/reject', 'reckonersite.views.reckoning.reject_reckoning_ajax'),
    (r'^ajax/reckoning/commentary/delete', 'reckonersite.views.reckoning.delete_reckoning_commentary'),
    (r'^ajax/reckoning/image/upload', 'reckonersite.views.reckoning.image_upload_ajax'),
    (r'^ajax/reckoning/image/download/(?P<id>\S+)', 'reckonersite.views.reckoning.image_download_ajax'),
    (r'^ajax/reckoning/image/add/(?P<id>\S+)', 'reckonersite.views.reckoning.image_add_ajax'),
    (r'^ajax/reckoning/image/delete/(?P<id>\S+)', 'reckonersite.views.reckoning.image_delete_ajax'),
    (r'^ajax/user/update/(?P<id>\w+)', 'reckonersite.views.user.update_reckoning_profile'),  
    (r'^ajax/user/(?P<id>\w+)', 'reckonersite.views.user.get_user_info_ajax'), 
    (r'^ajax/vote/update/(?P<reckoning_id>\w+?)/(?P<user_id>\w+?)/(?P<answer_index>\w+?)', 'reckonersite.views.vote.update_reckoning_vote'),
    # Examples:
    # url(r'^$', 'reckonersite.views.home', name='home'),
    # url(r'^reckonersite/', include('reckonersite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)