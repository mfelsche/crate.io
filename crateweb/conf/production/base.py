import os
import urlparse

from ..base import *

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "formatters": {
        "simple": {
            "format": "%(levelname)s %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple"
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "sentry": {
            "level": "ERROR",
            "class": "raven.contrib.django.handlers.SentryHandler",
        },
    },
    "root": {
        "handlers": ["console", "sentry"],
        "level": "INFO",
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "sentry.errors": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
    }
}

if "DATABASE_URL" in os.environ:
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    DATABASES = {
        "default": {
            "ENGINE": {
                "postgres": "django.db.backends.postgresql_psycopg2"
            }[url.scheme],
            "NAME": url.path[1:],
            "USER": url.username,
            "PASSWORD": url.password,
            "HOST": url.hostname,
            "PORT": url.port
        }
    }

if "REDIS_URL" in os.environ:
    urlparse.uses_netloc.append("redis")
    url = urlparse.urlparse(os.environ["REDIS_URL"])

    REDIS = {
        "default": {
            "HOST": url.hostname,
            "PORT": url.port,
            "PASSWORD": url.password,
        }
    }

    CACHES = {
       "default": {
            "BACKEND": "redis_cache.RedisCache",
            "LOCATION": "%(HOST)s:%(PORT)s" % REDIS["default"],
            "KEY_PREFIX": "cache",
            "OPTIONS": {
                "DB": 0,
                "PASSWORD": REDIS["default"]["PASSWORD"],
            }
        }
    }

    PYPI_DATASTORE = "default"

    LOCK_DATASTORE = "default"

    # Celery Broker
    BROKER_TRANSPORT = "redis"

    BROKER_HOST = REDIS["default"]["HOST"]
    BROKER_PORT = REDIS["default"]["PORT"]
    BROKER_PASSWORD = REDIS["default"]["PASSWORD"]
    BROKER_VHOST = "0"

    BROKER_POOL_LIMIT = 10

    # Celery Results
    CELERY_RESULT_BACKEND = "redis"

    CELERY_REDIS_HOST = REDIS["default"]["HOST"]
    CELERY_REDIS_PORT = REDIS["default"]["PORT"]
    CELERY_REDIS_PASSWORD = REDIS["default"]["PORT"]

SITE_ID = 3

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

SERVER_EMAIL = "server@crate.io"
DEFAULT_FROM_EMAIL = "support@crate.io"

PACKAGE_FILE_STORAGE = "storages.backends.s3boto.S3BotoStorage"
PACKAGE_FILE_STORAGE_OPTIONS = {
    "bucket": os.environ["PACKAGE_BUCKET"],
    "custom_domain": os.environ["PACKAGE_DOMAIN"],
}

DEFAULT_FILE_STORAGE = "storages.backends.s3boto.S3BotoStorage"
STATICFILES_STORAGE = "crateweb.storage.CachedStaticS3BotoStorage"

STATICFILES_S3_OPTIONS = {
    "bucket": "crate-static-production",
    "custom_domain": "dtl9zya2lik3.cloudfront.net",
    "secure_urls": True,
}

STATIC_URL = "https://dtl9zya2lik3.cloudfront.net/"

ADMIN_MEDIA_PREFIX = STATIC_URL + "admin/"

AWS_STORAGE_BUCKET_NAME = "crate-media-production"
AWS_S3_CUSTOM_DOMAIN = "media.crate-cdn.com"

AWS_STATS_BUCKET_NAME = "crate-logs"
AWS_STATS_LOG_REGEX = "^(cloudfront\.production/|cloudfront/production/packages/)"

INTERCOM_APP_ID = "79qt2qu3"

SIMPLE_API_URL = "https://simple.crate.io/"

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31556926
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

SECRET_KEY = os.environ["SECRET_KEY"]

EMAIL_HOST = os.environ["EMAIL_HOST"]
EMAIL_PORT = int(os.environ["EMAIL_PORT"])
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
EMAIL_USE_TLS = True

AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]

INTERCOM_USER_HASH_KEY = os.environ["INTERCOM_USER_HASH_KEY"]

GITHUB_APP_ID = os.environ["GITHUB_APP_ID"]
GITHUB_API_SECRET = os.environ["GITHUB_API_SECRET"]

BITBUCKET_CONSUMER_KEY = os.environ["BITBUCKET_CONSUMER_KEY"]
BITBUCKET_CONSUMER_SECRET = os.environ["BITBUCKET_CONSUMER_SECRET"]
