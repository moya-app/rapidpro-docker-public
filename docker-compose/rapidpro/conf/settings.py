# For full options, please see https://github.com/rapidpro/rapidpro/blob/main/temba/settings_common.py and https://github.com/rapidpro/rapidpro/blob/main/temba/settings.py.dev
import copy
import warnings

from .settings_common import *  # noqa

# Modify for each deploy
SECRET_KEY = "soarcudsarocudsboskab"

# may be an absolute URL to /media (like http://localhost:8000/media) or AWS S3
STORAGE_URL = "/media"
FLOW_FROM_EMAIL = "Temba <no-reply@temba.io>"

DEBUG = True
DJANGO_DEBUG = DEBUG

ADMINS = ()

# -----------------------------------------------------------------------------------
# set the mail settings, override these in your settings.py
# if your site was at http://temba.io, it might look like this:
# -----------------------------------------------------------------------------------
#EMAIL_HOST = "smtp.sendgrid.net"
#EMAIL_PORT = 587
#DEFAULT_FROM_EMAIL = ""
#EMAIL_HOST_USER = "apikey"
#EMAIL_HOST_PASSWORD = ""
#EMAIL_USE_TLS = True
#EMAIL_TIMEOUT = 10
#SEND_EMAILS = True

# -----------------------------------------------------------------------------------
# Add a custom brand for development
# -----------------------------------------------------------------------------------

DEFAULT_PLAN = WORKSPACE_PLAN

SERVER_ADDRESS = os.environ.get("SERVER_ADDRESS", "example.com")
BRANDING = {
    "rapidpro.io": {
        "slug": "rapidpro",
        "name": "RapidPro",
        "org": "UNICEF",
        "colors": dict(primary="#0c6596"),
        "styles": ["brands/rapidpro/font/style.css"],
        "default_plan": TOPUP_PLAN,
        "welcome_topup": 1000,
        "email": "join@rapidpro.io",
        "support_email": "support@rapidpro.io",
        "link": "https://app.rapidpro.io",
        "docs_link": "http://docs.rapidpro.io",
        "domain": "app.rapidpro.io",
        "ticket_domain": "tickets.rapidpro.io",
        "favico": "brands/rapidpro/rapidpro.ico",
        "splash": "brands/rapidpro/splash.jpg",
        "logo": "images/logo-dark.svg",
        "allow_signups": True,
        "tiers": dict(multi_user=0, multi_org=0),
        "welcome_packs": [dict(size=5000, name="Demo Account"), dict(size=100000, name="UNICEF Account")],
        "title": "Visually build nationally scalable mobile applications",
        "description": "Visually build nationally scalable mobile applications from anywhere in the world.",
        "credits": "Copyright &copy; 2012-2022 UNICEF, Nyaruka. All Rights Reserved.",
    }
}
DEFAULT_BRAND = os.environ.get("DEFAULT_BRAND", "rapidpro.io")

# Throttles for API calls on a per-org basis. Can be overridden by
# orgs_org.api_rates dict in the db on a per-org level.
DEFAULT_API_RATE = "3600/hour"
REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {
    "v2": DEFAULT_API_RATE,
    "v2.contacts": DEFAULT_API_RATE,
    "v2.messages": DEFAULT_API_RATE,
    "v2.broadcasts": "36000/hour",
    "v2.runs": DEFAULT_API_RATE,
}


# set our domain on our brands to our tunnel domain if set
#localhost_domain = os.environ.get("LOCALHOST_TUNNEL_DOMAIN")
#if localhost_domain is not None:
#    for b in BRANDING.values():
#        b["domain"] = localhost_domain

COMPRESS_OFFLINE_CONTEXT = []
for brand in BRANDING.values():
    context = dict(STATIC_URL=STATIC_URL, base_template="frame.html", debug=False, testing=False)
    context["brand"] = dict(slug=brand["slug"], styles=brand["styles"])
    COMPRESS_OFFLINE_CONTEXT.append(context)

# allow all hosts in dev
ALLOWED_HOSTS = ["*"]

# -----------------------------------------------------------------------------------
# Need a PostgreSQL database with postgis extension installed.
# -----------------------------------------------------------------------------------
_default_database_config = {
    "ENGINE": "django.contrib.gis.db.backends.postgis",
    "NAME": "rapidpro",
    "USER": "rapidpro",
    "PASSWORD": "ayXVXnIl4MHQtdGXI2U",
    "HOST": "db",
    "PORT": "5432",
    "ATOMIC_REQUESTS": True,
    "CONN_MAX_AGE": 60,
    "OPTIONS": {},
    "DISABLE_SERVER_SIDE_CURSORS": True,
}

# installs can provide a default connection and an optional read-only connection (e.g. a separate read replica) which
# will be used for certain fetch operations
DATABASES = {"default": _default_database_config, "readonly": _default_database_config.copy()}

# -----------------------------------------------------------------------------------
# Redis & Cache Configuration
# -----------------------------------------------------------------------------------
REDIS_HOST = 'redis'
REDIS_DB = 15
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://%s:%s/%s" % (REDIS_HOST, REDIS_PORT, REDIS_DB),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

INTERNAL_IPS = iptools.IpRangeList("127.0.0.1", "172.0.0.0/8")  # network block for docker-compose
HOSTNAME = "rapidpro"


# -----------------------------------------------------------------------------------
# Mailroom - localhost for dev, no auth token
# -----------------------------------------------------------------------------------
MAILROOM_URL = os.environ.get('MAILROOM_URL')
MAILROOM_AUTH_TOKEN = os.environ.get('MAILROOM_AUTH_TOKEN')

# -----------------------------------------------------------------------------------
# Load development apps
# -----------------------------------------------------------------------------------
INSTALLED_APPS = INSTALLED_APPS + ("storages",)

# -----------------------------------------------------------------------------------
# In development, add in extra logging for exceptions and the debug toolbar
# -----------------------------------------------------------------------------------
MIDDLEWARE = ("temba.middleware.ExceptionMiddleware",) + MIDDLEWARE

# -----------------------------------------------------------------------------------
# Async tasks using Celery
# -----------------------------------------------------------------------------------
CELERY_RESULT_BACKEND = None
CELERY_BROKER_URL = "redis://%s:%d/%d" % (REDIS_HOST, REDIS_PORT, REDIS_DB)

#CELERY_TASK_ALWAYS_EAGER = True
#CELERY_TASK_EAGER_PROPAGATES = True

# -----------------------------------------------------------------------------------
# This setting throws an exception if a naive datetime is used anywhere. (they should
# always contain a timezone)
# -----------------------------------------------------------------------------------
warnings.filterwarnings(
    "error", r"DateTimeField .* received a naive datetime", RuntimeWarning, r"django\.db\.models\.fields"
)

# -----------------------------------------------------------------------------------
# Make our sitestatic URL be our static URL on development
# -----------------------------------------------------------------------------------
STATIC_URL = "/sitestatic/"


CHANNEL_TYPES = [
    "temba.channels.types.arabiacell.ArabiaCellType",
    "temba.channels.types.whatsapp.WhatsAppType",
    "temba.channels.types.whatsapp_cloud.WhatsAppCloudType",
    "temba.channels.types.dialog360.Dialog360Type",
    "temba.channels.types.zenvia_whatsapp.ZenviaWhatsAppType",
    "temba.channels.types.twilio.TwilioType",
    "temba.channels.types.twilio_whatsapp.TwilioWhatsappType",
    "temba.channels.types.twilio_messaging_service.TwilioMessagingServiceType",
    "temba.channels.types.signalwire.SignalWireType",
    "temba.channels.types.vonage.VonageType",
    "temba.channels.types.africastalking.AfricasTalkingType",
    "temba.channels.types.blackmyna.BlackmynaType",
    "temba.channels.types.bongolive.BongoLiveType",
    "temba.channels.types.burstsms.BurstSMSType",
    "temba.channels.types.chikka.ChikkaType",
    "temba.channels.types.clickatell.ClickatellType",
    "temba.channels.types.clickmobile.ClickMobileType",
    "temba.channels.types.clicksend.ClickSendType",
    "temba.channels.types.dartmedia.DartMediaType",
    "temba.channels.types.dmark.DMarkType",
    "temba.channels.types.external.ExternalType",
    "temba.channels.types.facebook.FacebookType",
    "temba.channels.types.facebookapp.FacebookAppType",
    "temba.channels.types.firebase.FirebaseCloudMessagingType",
    "temba.channels.types.freshchat.FreshChatType",
    "temba.channels.types.globe.GlobeType",
    "temba.channels.types.highconnection.HighConnectionType",
    "temba.channels.types.hormuud.HormuudType",
    "temba.channels.types.hub9.Hub9Type",
    "temba.channels.types.i2sms.I2SMSType",
    "temba.channels.types.infobip.InfobipType",
    "temba.channels.types.jasmin.JasminType",
    "temba.channels.types.jiochat.JioChatType",
    "temba.channels.types.junebug.JunebugType",
    "temba.channels.types.kaleyra.KaleyraType",
    "temba.channels.types.kannel.KannelType",
    "temba.channels.types.line.LineType",
    "temba.channels.types.m3tech.M3TechType",
    "temba.channels.types.macrokiosk.MacrokioskType",
    "temba.channels.types.mtarget.MtargetType",
    "temba.channels.types.mblox.MbloxType",
    "temba.channels.types.messangi.MessangiType",
    "temba.channels.types.novo.NovoType",
    "temba.channels.types.playmobile.PlayMobileType",
    "temba.channels.types.plivo.PlivoType",
    "temba.channels.types.redrabbit.RedRabbitType",
    "temba.channels.types.shaqodoon.ShaqodoonType",
    "temba.channels.types.smscentral.SMSCentralType",
    "temba.channels.types.start.StartType",
    "temba.channels.types.telegram.TelegramType",
    "temba.channels.types.telesom.TelesomType",
    "temba.channels.types.thinq.ThinQType",
    "temba.channels.types.twiml_api.TwimlAPIType",
    "temba.channels.types.twitter.TwitterType",
    "temba.channels.types.twitter_legacy.TwitterLegacyType",
    "temba.channels.types.verboice.VerboiceType",
    "temba.channels.types.viber_public.ViberPublicType",
    "temba.channels.types.vk.VKType",
    "temba.channels.types.wavy.WavyType",
    "temba.channels.types.wechat.WeChatType",
    "temba.channels.types.yo.YoType",
    "temba.channels.types.zenvia.ZenviaType",
    "temba.channels.types.zenvia_sms.ZenviaSMSType",
    "temba.channels.types.android.AndroidType",
    "temba.channels.types.discord.DiscordType",
    "temba.channels.types.rocketchat.RocketChatType",
    "temba.channels.types.instagram.InstagramType",
]

RETENTION_PERIODS = {
    "channellog": timedelta(days=3),
    "eventfire": timedelta(days=90),  # matches default rp-archiver behavior
    "flowsession": timedelta(days=7),
    "flowstart": timedelta(days=7),
    "httplog": timedelta(days=3),
    "syncevent": timedelta(days=7),
    "webhookevent": timedelta(hours=48),
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_DIR, "../templates"),
            os.path.join(PROJECT_DIR, "../node_modules/@nyaruka/temba-components/dist/templates"),
        ],
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
                "temba.context_processors.branding",
                "temba.context_processors.config",
                "temba.orgs.context_processors.user_group_perms_processor",
                "temba.channels.views.channel_status_processor",
                "temba.orgs.context_processors.settings_includer",
                "temba.orgs.context_processors.user_orgs_for_brand",
            ],
            "loaders": [
                "temba.utils.haml.HamlFilesystemLoader",
                "temba.utils.haml.HamlAppDirectoriesLoader",
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "debug": False if TESTING else DEBUG,
        },
    }
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "root": {"level": "WARNING", "handlers": ["console"]},
    "formatters": {"verbose": {"format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"}},
    "handlers": {
        "console": {"level": "DEBUG", "class": "logging.StreamHandler", "formatter": "verbose"},
        "null": {"class": "logging.NullHandler"},
    },
    "loggers": {
        "pycountry": {"level": "ERROR", "handlers": ["console"], "propagate": False},
        "django.security.DisallowedHost": {"handlers": ["null"], "propagate": False},
        "django.db.backends": {"level": "ERROR", "handlers": ["console"], "propagate": False},
        "temba.formax": {"level": "DEBUG" if DEBUG else "ERROR", "handlers": ["console"], "propagate": False},
    },
}

# When in production, enable this. If you change a theme, or clear sitestatic, you'll need to restart redis to force a cache regeneration.
COMPRESS_ENABLED = True

#COMPRESS_OFFLINE = True
#COMPRESS_CSS_HASHING_METHOD = "content"
#COMPRESS_OFFLINE_CONTEXT = dict(
#    STATIC_URL=STATIC_URL, base_template="frame.html", brand=BRANDING[DEFAULT_BRAND], debug=False, testing=False
#)
#
