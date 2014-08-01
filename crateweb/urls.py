from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

import jutils.ji18n.translate
jutils.ji18n.translate.patch()

from crate.web.search.views import Search


handler500 = "pinax.views.server_error"


urlpatterns = patterns("",
    url(r"^$", Search.as_view(), name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^admin_tools/", include("admin_tools.urls")),
    url(r"^packages/", include("crate.web.packages.urls")),

    url(r"^stats/", include("crate.web.packages.stats.urls")),
    url(r"^externally-hosted/$", "crate.web.packages.views.fuck_the_status_quo"),
    url(r"^", include("crate.web.search.urls")),
)


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
    )
