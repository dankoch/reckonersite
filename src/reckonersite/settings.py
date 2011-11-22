#==========================CUSTOM SETTINGS======================================
from mongoengine import connect

# Application Name -- used for identifying permissions and other labeling
APPLICATION_NAME='reckonersite'

# Site Name -- Used for Display Purposes
SITE_NAME='The Reckoner!'

# Triggers Django Debugging Console
DEBUG = True

# Host Name Contacted By The Reckoner Site Client
RECKON_CONTENT_SERVICES_HOST = 'http://localhost:8080/reckoner-content-services'

# Root URL for the website
SITE_ROOT = 'http://www.thereckoner.net'

# Information Used to Communicate With Facebook
# Each element is used as part of the OAUTH verification process to build the correct URLs for
# the server-side authentication process.

FACEBOOK_APP_ID = '194559340610034'
FACEBOOK_APP_SECRET = 'ff01f6b6c13c50b5685f15f9a6b70bb2'
FACEBOOK_REDIRECT_URL = 'http://localhost:8000/login/facebook'

FACEBOOK_GRAPH_URL = "https://graph.facebook.com"
FACEBOOK_OAUTH_URL = "https://www.facebook.com/dialog/oauth"
FACEBOOK_GRAPH_TOKEN_URL = "https://graph.facebook.com/oauth/access_token"

FACEBOOK_SCOPE = "offline_access"

# Additional settings used for FB JDK Integration
FACEBOOK_PAGE_ID= '185721918154268'
FACEBOOK_ADMIN_ID= '613012'
FACEBOOK_SITE_TYPE= 'website'

# Information Used to Communicate With Google
# Each element is used as part of the OAUTH verification process to build the correct URLs for
# the server-side authentication process.

GOOGLE_APP_ID="565621549243.apps.googleusercontent.com"
GOOGLE_APP_SECRET="8QdIGfIitnM_Psv1YAEuFgHn"
GOOGLE_REDIRECT_URL="http://localhost:8000/login/google"

GOOGLE_API_URL=""
GOOGLE_API_OAUTH_URL="https://accounts.google.com/o/oauth2/auth"
GOOGLE_API_TOKEN_URL="https://accounts.google.com/o/oauth2/token"

GOOGLE_SCOPE = "https://www.googleapis.com/auth/plus.me"

# Connect to MongoDB.  The database is only used for session persistence.
connect ('session')
SESSION_ENGINE = 'mongoengine.django.sessions'

# Information used to configure logging settings
FILE_LOG_LOCATION = '/Users/danko/Documents/development/logs'
STANDARD_LOGGER = 'reckonersite.standard'

# Keys used to store session information
RECKONER_API_SESSION_ID = 'rcktk'
LAST_SITE_TOKEN_ID = 'lastsite'

# Settings used for sending emails
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'contact@reckonlabs.org'
EMAIL_HOST_PASSWORD = '_qazwsx_EDCRFV'
EMAIL_USE_TLS = True

# Destination used for Contact Us form
CONTACT_US_EMAIL='contact@reckonlabs.org'

# Settings used for CAPTCHA
#localhost
CAPTCHA_PRIVATE_KEY='6LcPKMoSAAAAAIJz6RqqoartHdB_QaJGvqrig00C'
CAPTCHA_PUBLIC_KEY='6LcPKMoSAAAAANk6sbcYgBuLDR611Fe1xXYanu4c'
#thereckoner.net
#CAPTCHA_PRIVATE_KEY='6LcQKMoSAAAAAPnslgNlrFeqYtHY9FgeN0fSq_kN' 
#CAPTCHA_PUBLIC_KEY='6LcQKMoSAAAAAFEu8H-CokaO6V4XETHJGBwuRe_W'

# Settings for creating the Reckoner XML Sitemap
XML_SITEMAP_LOCATION='/Users/danko/Desktop'

# Miscellaneous Settings
## Sentinel used to mark fields as deleted for Reckoning update calls
RECKONING_UPDATE_DELETE_SENTINEL = "null"

#==========================END CUSTOM SETTINGS==================================

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mongodb', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#        'NAME': 'reckonerdb',                      # Or path to database file if using sqlite3.
#        'USER': '',                      # Not used with sqlite3.
#        'PASSWORD': '',                  # Not used with sqlite3.
#        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
#        'PORT': '27017',                      # Set to empty string for default. Not used with sqlite3.
#    }
#}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
#TIME_ZONE = 'None'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "/Users/danko/Documents/development/reckonersite/src/reckonersite/static",
)

TEMPLATE_CONTEXT_PROCESSORS = ("django.core.context_processors.debug",
                               "django.core.context_processors.i18n",
                               "django.core.context_processors.media",
                               "django.core.context_processors.static",
                               "django.contrib.messages.context_processors.messages",
                               'reckonersite.context_processors.reckonerauth.set_user_info', 
                               'reckonersite.context_processors.reckoningcontext.set_reckoning_context',            
                               'reckonersite.context_processors.socialconnections.set_social_info',)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '5fpo2i9xi6ko=k5+%!le7#0ykq%)heiul5@0ev@ehhnt-8378*'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'reckonersite.middleware.reckonerauth.ReckonerAuthMiddleware',
    'reckonersite.middleware.breadcrumb.BreadcrumbMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'reckonersite.urls'

TEMPLATE_DIRS = (
    '/Users/danko/Documents/development/reckonersite/src/reckonersite/templates',
    
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'reckonersite',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'standard': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
            'formatter': 'standard'
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'standard'
        },
        'file_log': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'maxBytes': 52428800,
            'backupCount': 5,
            'filename': FILE_LOG_LOCATION + 'reckonsite'
        }
    },
    'loggers': {
        'reckonersite.standard': {
            'handlers': ['console', 'file_log'],
            'level': 'INFO'
        }
    }
}
