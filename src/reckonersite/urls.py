from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^post-reckoning-welcome', 'reckonersite.views.reckoning.post_reckoning_welcome'),
    (r'^post-reckoning', 'reckonersite.views.reckoning.post_reckoning'),
    (r'^thanks-for-playing', 'reckonersite.views.reckoning.post_reckoning_thanks'),
    (r'^gosh-darn-it-to-heck', 'reckonersite.views.reckoning.reckoning_fail'),
    (r'^notes/reckoning/comment/flag/(?P<id>\w+)', 'reckonersite.views.note.post_reckoning_comment_flag'),
    (r'^notes/reckoning/flag/(?P<id>\w+)', 'reckonersite.views.note.post_reckoning_flag'),
    (r'^notes/reckoning/comment/favorite/(?P<id>\w+)', 'reckonersite.views.note.post_reckoning_comment_favorite'),
    (r'^notes/reckoning/favorite/(?P<id>\w+)', 'reckonersite.views.note.post_reckoning_favorite'),
    (r'^comment/reckoning/post', 'reckonersite.views.reckoning.post_reckoning_comment'),    
    (r'^comment/reckoning/update', 'reckonersite.views.reckoning.update_reckoning_comment'),
    (r'^comment/reckoning/delete', 'reckonersite.views.reckoning.delete_reckoning_comment'),
    (r'^vote/reckoning', 'reckonersite.views.reckoning.vote_reckoning'), 
    (r'^open-reckonings', 'reckonersite.views.reckoning.get_open_reckonings'),
    (r'^finished-reckonings', 'reckonersite.views.reckoning.get_closed_reckonings'),
    (r'^reckonings/tag/(?P<tag>\S+)', 'reckonersite.views.reckoning.get_tagged_reckonings'),
    (r'^random-reckoning', 'reckonersite.views.reckoning.get_random_reckoning'),
    (r'^reckoning/update', 'reckonersite.views.reckoning.update_reckoning_ajax'),
    (r'^reckoning/reject', 'reckonersite.views.reckoning.reject_reckoning_ajax'),
    (r'^reckoning/commentary/delete', 'reckonersite.views.reckoning.delete_reckoning_commentary'),  
    (r'^reckoning/(?P<id>\w+?)/(?P<title>\S+)', 'reckonersite.views.reckoning.get_reckoning'),   
    (r'^user/bio/(?P<id>\w+)', 'reckonersite.views.user.update_reckoning_bio'),   
    (r'^user/ajax/(?P<id>\w+)', 'reckonersite.views.user.get_user_info_ajax'), 
    (r'^user/(?P<id>\w+?)/(?P<name>\S+)', 'reckonersite.views.user.get_user_profile'),
    (r'^login/tricky-ol-google', 'reckonersite.views.login.rejected_login_bad_google'),
    (r'^login/google', 'reckonersite.views.login.login_google'),
    (r'^login/facebook', 'reckonersite.views.login.login_facebook'),
    (r'^login/howdy', 'reckonersite.views.login.logged_in'),
    (r'^login/no-sweat', 'reckonersite.views.login.rejected_login'),
    (r'^login/logout', 'reckonersite.views.login.logout'),       
    (r'^login', 'reckonersite.views.login.login_page'),
    (r'^admin/flagged', 'reckonersite.views.admin.flag_summary_page'),
    (r'^admin/user-permissions', 'reckonersite.views.admin.user_permissions_page'),
    (r'^admin/approval', 'reckonersite.views.admin.reckoning_approval_page'),
    (r'^admin', 'reckonersite.views.admin.admin_page'),
    (r'^$', 'reckonersite.views.home.home_page'),            
    # Examples:
    # url(r'^$', 'reckonersite.views.home', name='home'),
    # url(r'^reckonersite/', include('reckonersite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
