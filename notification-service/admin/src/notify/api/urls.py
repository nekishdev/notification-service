from django.urls import path, include

urlpatterns = (
    path('v1/', include('notify.api.v1.urls')),
)
