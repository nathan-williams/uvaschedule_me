from django.conf.urls import patterns, include, url
from django.contrib import admin
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hooslist.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index),
    url(r'^index/', views.index),
    url(r'^about/', views.about),
    url(r'^schedule/', views.schedule),
    url(r'^update/', views.update),
    url(r'^error/', views.error),
)