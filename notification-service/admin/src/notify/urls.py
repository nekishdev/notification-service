"""api URL Configurations."""

from django.urls import include, path

urlpatterns = [
    path('v1/', include('notify.api.v1.urls')),
]
