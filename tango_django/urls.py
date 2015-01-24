from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

from rango import views
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', views.index, name='index'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^rango/', include('rango.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
					