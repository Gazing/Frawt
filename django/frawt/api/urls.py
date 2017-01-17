from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='api_index'),
    url(r'^time$', views.get_server_time, name='api_time'),
    url(r'^rooms/available/$', views.find_available, name='api_available'),
    url(r'^rooms/(.+)/schedule/(.*)$', views.get_schedule, name='api_room_schedule'),
]