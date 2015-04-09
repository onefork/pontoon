"""Django settings for Pontoon."""
import logging
import os
import socket

from django.utils.functional import lazy

import dj_database_url

from funfactory.manage import ROOT, path


# Environment-dependent settings. These are loaded from environment
# variables.

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ['SECRET_KEY']

# Is this a dev instance?
DEV = os.environ.get('DJANGO_DEV', 'False') != 'False'

DEBUG = TEMPLATE_DEBUG = os.environ.get('DJANGO_DEBUG', 'False') != 'False'

ADMINS = MANAGERS = (
    (os.environ.get('ADMIN_NAME', ''),
     os.environ.get('ADMIN_EMAIL', '')),
)

DATABASES = {
    'default': dj_database_url.config(default='mysql://root@localhost/pontoon')
}

SESSION_COOKIE_HTTPONLY = os.environ.get('SESSION_COOKIE_HTTPONLY', 'True') != 'False'
SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'True') != 'False'

HMAC_KEYS = {
    'hmac_key': os.environ['HMAC_KEY'],
}

SITE_URL = os.environ['SITE_URL']

# Microsoft Translator API Key
MICROSOFT_TRANSLATOR_API_KEY = os.environ.get('MICROSOFT_TRANSLATOR_API_KEY', '')

# Google Analytics Key
GOOGLE_ANALYTICS_KEY = os.environ.get('GOOGLE_ANALYTICS_KEY', '')

# Mozillians API Key
MOZILLIANS_API_KEY = os.environ.get('MOZILLIANS_API_KEY', '')


# Environment-independent settings. These shouldn't have to change
# between server environments.
ROOT_URLCONF = 'pontoon.urls'

INSTALLED_APPS = (
    'pontoon.base',
    'pontoon.administration',
    'pontoon.intro',

    # Django contrib apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    # Third-party apps, patches, fixes
    'commonware.response.cookies',
    'compressor',
    'cronjobs',
    'django_browserid',
    'django_nose',
    'djcelery',
    'funfactory',
    'product_details',
    'session_csrf',
    'south',
    'tower',
)

MIDDLEWARE_CLASSES = (
    'multidb.middleware.PinningRouterMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'session_csrf.CsrfMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'commonware.middleware.FrameOptionsHeader',
    'mobility.middleware.DetectMobileMiddleware',
    'mobility.middleware.XMobileMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'session_csrf.context_processor',
    'django.contrib.messages.context_processors.messages',
    'funfactory.context_processors.i18n',
    'funfactory.context_processors.globals',
    'django_browserid.context_processors.browserid',
)

TEMPLATE_LOADERS = (
    'jingo.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    path('templates'),
)

AUTHENTICATION_BACKENDS = [
    'django_browserid.auth.BrowserIDBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Paths containing translation files for the site.
LOCALE_PATHS = (
    os.path.join(ROOT, 'pontoon', 'locale'),
)

# Template directories that contain Django templates instead of Jinja.
JINGO_EXCLUDE_APPS = [
    'admin',
    'registration',
]

# Tells the extract script what files to look for L10n in and what function
# handles the extraction. The Tower library expects this.
DOMAIN_METHODS = {
    'messages': [
        ('pontoon/**.py',
            'tower.management.commands.extract.extract_tower_python'),
        ('pontoon/**/templates/**.html',
            'tower.management.commands.extract.extract_tower_template'),
        ('templates/**.html',
            'tower.management.commands.extract.extract_tower_template'),
    ]
}

# Required for storing additional information about users
AUTH_PROFILE_MODULE = 'base.UserProfile'

DATABASE_ROUTERS = ('multidb.PinningMasterSlaveRouter',)

# Site ID is used by Django's Sites framework.
SITE_ID = 1

## Media and templates.

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = path('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = path('static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Storage of static files
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_CSS_FILTERS = (
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter'
)
COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

# Path to Java. Used for compress_assets.
JAVA_BIN = '/usr/bin/java'

def JINJA_CONFIG():
    return {
        'extensions': [
            'tower.template.i18n',
            'jinja2.ext.do',
            'jinja2.ext.with_',
            'jinja2.ext.loopcontrols'
        ],
        'finalize': lambda x: x if x is not None else ''
    }

## Auth
# The first hasher in this list will be used for new passwords.
# Any other hasher in the list can be used for existing passwords.
# Playdoh ships with Bcrypt+HMAC by default because it's the most secure.
# To use bcrypt, fill in a secret HMAC key in your local settings.
BASE_PASSWORD_HASHERS = (
    'django_sha2.hashers.BcryptHMACCombinedPasswordVerifier',
    'django_sha2.hashers.SHA512PasswordHasher',
    'django_sha2.hashers.SHA256PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
)

from django_sha2 import get_password_hashers
PASSWORD_HASHERS = get_password_hashers(BASE_PASSWORD_HASHERS, HMAC_KEYS)

## Logging
LOG_LEVEL = logging.INFO
HAS_SYSLOG = True
SYSLOG_TAG = "http_app_pontoon"  # Change this after you fork.
LOGGING_CONFIG = None
LOGGING = {}

# CEF Logging
CEF_PRODUCT = 'Pontoon'
CEF_VENDOR = 'Mozilla'
CEF_VERSION = '0'
CEF_DEVICE_VERSION = '0'

## Tests
TEST_RUNNER = 'test_utils.runner.RadicalTestSuiteRunner'

## Celery

# True says to simulate background tasks without actually using celeryd.
# Good for local development in case celeryd is not running.
CELERY_ALWAYS_EAGER = True

BROKER_CONNECTION_TIMEOUT = 0.1
CELERY_RESULT_BACKEND = 'amqp'
CELERY_IGNORE_RESULT = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

# Time in seconds before celery.exceptions.SoftTimeLimitExceeded is raised.
# The task can catch that and recover but should exit ASAP.
CELERYD_TASK_SOFT_TIME_LIMIT = 60 * 2

## Arecibo
# when ARECIBO_SERVER_URL is set, it can use celery or the regular wrapper
ARECIBO_USES_CELERY = True

# django-browserid
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL_FAILURE = '/'

# Should robots.txt deny everything or disallow a calculated list of
# URLs we don't want to be crawled?  Default is false, disallow
# everything.
ENGAGE_ROBOTS = False

# Always generate a CSRF token for anonymous users.
ANON_ALWAYS = True

# For absolute urls
try:
    DOMAIN = socket.gethostname()
except socket.error:
    DOMAIN = 'localhost'
PROTOCOL = "http://"
PORT = 80

## django-mobility
MOBILE_COOKIE = 'mobile'

# Names for slave databases from the DATABASES setting.
SLAVE_DATABASES = []

## Internationalization.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Gettext text domain
TEXT_DOMAIN = 'messages'
STANDALONE_DOMAINS = [TEXT_DOMAIN, 'javascript']
TOWER_KEYWORDS = {'_lazy': None}
TOWER_ADD_HEADERS = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-US'

## Accepted locales

# Tells the product_details module where to find our local JSON files.
# This ultimately controls how LANGUAGES are constructed.
PROD_DETAILS_DIR = path('lib/product_details_json')

# On dev instances, the list of accepted locales defaults to the contents of
# the `locale` directory within a project module or, for older Playdoh apps,
# the root locale directory.  A localizer can add their locale in the l10n
# repository (copy of which is checked out into `locale`) in order to start
# testing the localization on the dev server.
import glob
import itertools
try:
    DEV_LANGUAGES = [
        os.path.basename(loc).replace('_', '-')
        for loc in itertools.chain(glob.iglob(ROOT + '/locale/*'),  # old style
                                   glob.iglob(ROOT + '/*/locale/*'))
        if (os.path.isdir(loc) and os.path.basename(loc) != 'templates')
    ]
except OSError:
    DEV_LANGUAGES = ('en-US',)

# On stage/prod, the list of accepted locales is manually maintained.  Only
# locales whose localizers have signed off on their work should be listed here.
PROD_LANGUAGES = (
    'en-US',
)

def lazy_lang_url_map():
    from django.conf import settings
    langs = settings.DEV_LANGUAGES if settings.DEV else settings.PROD_LANGUAGES
    return dict([(i.lower(), i) for i in langs])

LANGUAGE_URL_MAP = lazy(lazy_lang_url_map, dict)()

# Override Django's built-in with our native names
def lazy_langs():
    from django.conf import settings
    from product_details import product_details
    langs = DEV_LANGUAGES if settings.DEV else settings.PROD_LANGUAGES
    return dict([(lang.lower(), product_details.languages[lang]['native'])
                 for lang in langs if lang in product_details.languages])

LANGUAGES = lazy(lazy_langs, dict)()

# Paths that don't require a locale code in the URL.
SUPPORTED_NONLOCALES = ['media', 'static', 'admin']

# Microsoft Translator Locales
MICROSOFT_TRANSLATOR_LOCALES = [
    'ar', 'bs-Latn', 'bg', 'ca', 'zh-CHS', 'zh-CHT', 'hr', 'cs', 'da', 'nl',
    'en', 'et', 'fi', 'fr', 'de', 'el', 'ht', 'he', 'hi', 'mww', 'hu', 'id',
    'it', 'ja', 'tlh', 'tlh-Qaak', 'ko', 'lv', 'lt', 'ms', 'mt', 'yua', 'no',
    'otq', 'fa', 'pl', 'pt', 'ro', 'ru', 'sr-Cyrl', 'sr-Latn', 'sk', 'sl',
    'es', 'sv', 'th', 'tr', 'uk', 'ur', 'vi', 'cy'
]

# Microsoft Terminology Service API Locales
MICROSOFT_TERMINOLOGY_LOCALES = [
    'af-za', 'am-et', 'ar-eg', 'ar-sa', 'as-in', 'az-latn-az', 'be-by',
    'bg-bg', 'bn-bd', 'bn-in', 'bs-cyrl-ba', 'bs-latn-ba', 'ca-es',
    'ca-es-valencia', 'chr-cher-us', 'cs-cz', 'cy-gb', 'da-dk', 'de-at',
    'de-ch', 'de-de', 'el-gr', 'en-au', 'en-ca', 'en-gb', 'en-ie', 'en-my',
    'en-nz', 'en-ph', 'en-sg', 'en-us', 'en-za', 'es-es', 'es-mx', 'es-us',
    'et-ee', 'eu-es', 'fa-ir', 'fi-fi', 'fil-ph', 'fr-be', 'fr-ca', 'fr-ch',
    'fr-fr', 'fr-lu', 'fuc-latn-sn', 'ga-ie', 'gd-gb', 'gl-es', 'gu-in',
    'guc-ve', 'ha-latn-ng', 'he-il', 'hi-in', 'hr-hr', 'hu-hu', 'hy-am',
    'id-id', 'ig-ng', 'is-is', 'it-ch', 'it-it', 'iu-latn-ca', 'ja-jp',
    'ka-ge', 'kk-kz', 'km-kh', 'kn-in', 'ko-kr', 'kok-in', 'ku-arab-iq',
    'ky-kg', 'lb-lu', 'lo-la', 'lt-lt', 'lv-lv', 'mi-nz', 'mk-mk', 'ml-in',
    'mn-mn', 'mr-in', 'ms-bn', 'ms-my', 'mt-mt', 'nb-no', 'ne-np', 'nl-be',
    'nl-nl', 'nn-no', 'nso-za', 'or-in', 'pa-arab-pk', 'pa-in', 'pl-pl',
    'prs-af', 'ps-af', 'pt-br', 'pt-pt', 'qut-gt', 'quz-pe', 'rm-ch', 'ro-ro',
    'ru-ru', 'rw-rw', 'sd-arab-pk', 'si-lk', 'sk-sk', 'sl-si', 'sp-xl',
    'sq-al', 'sr-cyrl-ba', 'sr-cyrl-rs', 'sr-latn-rs', 'sv-se', 'sw-ke',
    'ta-in', 'te-in', 'tg-cyrl-tj', 'th-th', 'ti-et', 'tk-tm', 'tl-ph',
    'tn-za', 'tr-tr', 'tt-ru', 'ug-cn', 'uk-ua', 'ur-pk', 'uz-latn-uz',
    'vi-vn', 'wo-sn', 'xh-za', 'yo-ng', 'zh-cn', 'zh-hk', 'zh-tw', 'zu-za',
]

# Contributors to exclude from Top Contributors list
EXCLUDE = []
