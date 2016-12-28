from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='api_index'),
    url(r'^rooms/current', views.find_current, name='current_api'),
    url(r'^time$', views.get_server_time, name='api_time'),
]