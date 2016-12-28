from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
        url(r'^rf.js', views.send_rf_js, name='rf.js'),
]