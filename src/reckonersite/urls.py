from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^post-reckoning', 'reckonersite.views.reckoning.post_reckoning'),
    (r'^thanks-for-playing', 'reckonersite.views.reckoning.post_reckoning_thanks'),
    (r'^gosh-darn-it-to-heck', 'reckonersite.views.reckoning.reckoning_fail'),
    (r'^reckoning/(?P<id>\w+?)/\S+', 'reckonersite.views.reckoning.get_reckoning'),
    (r'^login/tricky-ol-google', 'reckonersite.views.login.rejected_login_bad_google'),
    (r'^login/google', 'reckonersite.views.login.login_google'),
    (r'^login/facebook', 'reckonersite.views.login.login_facebook'),
    (r'^login/howdy', 'reckonersite.views.login.logged_in'),
    (r'^login/no-sweat', 'reckonersite.views.login.rejected_login'),
    (r'^login/logout', 'reckonersite.views.login.logout'),       
    (r'^login', 'reckonersite.views.login.login_page'),
    (r'^$', 'reckonersite.views.home.home_page'),            
    # Examples:
    # url(r'^$', 'reckonersite.views.home', name='home'),
    # url(r'^reckonersite/', include('reckonersite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
