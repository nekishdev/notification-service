from django.urls import path

from . import views

urlpatterns = (
    path("notifications/bodytemplates/<uuid:pk>/", views.TemplatesBodyDetailApi.as_view()),
    path("notifications/bodytemplates/", views.TemplatesBodyListApi.as_view()),
    path("notifications/notifytemplates/<uuid:pk>/", views.TemplatesNotifyDetailApi.as_view()),
    path("notifications/notifytemplates/", views.TemplatesNotifyListApi.as_view()),
    path("notifications/", views.NotificationsListApi.as_view()),
    path("notifications/<uuid:pk>/", views.NotificationsDetailApi.as_view()),
)
