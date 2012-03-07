from django.conf.urls.defaults import patterns, include, url
from django_sandbox import views,settings,forms
from django.contrib.auth.views import login, logout
from django_authopenid.views import signin, password_change, signout, register
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from registration import views as reg_views 
admin.autodiscover()

urlpatterns = patterns('',
                      # url(r'^favicon\.ico$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT+'/django.png'}),
                       url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
                       url(r'^account/signin/$',signin),
                       url(r'^account/register/$',register),
                       url(r'^activate/(?P<activation_key>\w+)/$', reg_views.activate, name='registration_activate'),
                       url(r'^account/logout/$',signout),
                       url(r'^account/profile/$',views.redirect_profile),
                       url(r'^account/profile/[\w\d\.]+/edit/$',views.edit_details),
                       url(r'^account/profile/[\w\d\.]+/change_password/$',password_change),
                       url(r'^account/profile/([\w\d\.]+)/$',views.profile_view),
                       url(r'^$', views.redirect_profile),
    # Examples:
    # url(r'^$', 'django_sandbox.views.home', name='home'),
    # url(r'^django_sandbox/', include('django_sandbox.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls),),
     url(r'^account/', include('django_authopenid.urls')),
)
