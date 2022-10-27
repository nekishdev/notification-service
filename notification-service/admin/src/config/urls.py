"""Project URL Configurations."""

from django.urls import include, path

from config import settings

urlpatterns = [
    path('api/', include('notify.api.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
