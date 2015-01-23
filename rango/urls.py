from django.conf.urls import patterns, include, url
from django.conf import settings
from rango import views
urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.index, name='index'),
    url(r'^add_category/$',views.add_category, name='add_category'),
    url(r'^category/(?P<category_name_slug>[\w-]+)/$', views.category, name='category'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$',views.user_login, name='login'),
    url(r'^restricted/$',views.restricted, name='restricted'),
    url(r'^logout/$',views.loggedout, name='logout'),
    # url(r'^blog/', include('blog.urls')),
)

