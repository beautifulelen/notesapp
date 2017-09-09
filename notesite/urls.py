# Django
from django.contrib import admin
from django.conf.urls import url

# REST Framework jwt
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from rest_framework.urlpatterns import format_suffix_patterns

# Notes App
from note import views


admin.autodiscover()

urlpatterns = [
    # Admin url
    url(r'^admin/', admin.site.urls),

    # JWT token auth and refresh
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),

    # Registration of new users
    url(r'^register/$', views.RegistrationView.as_view()),

    # Notes CBV endpoints
    url(r'^notes/$', views.NoteList.as_view(), name='note'),
    url(r'^notes/(?P<pk>[0-9]+)$', views.NoteDetail.as_view(), name='note-detail'),

]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json'])