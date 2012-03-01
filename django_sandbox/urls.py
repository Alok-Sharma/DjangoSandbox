from django.conf.urls.defaults import patterns, include, url
from django_sandbox import views,settings
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^favicon\.ico$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT+'/django.png'}),
                       url(r'^tmp/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
                       url(r'^accounts/login/$',login),
                       url(r'^accounts/register/$',views.register),
                       url(r'^accounts/logout/$',logout),
                       url(r'^accounts/profile/$',views.redirect_profile),
                       url(r'^accounts/profile/[\w\d\.]+/edit/$',views.edit_details),
                       url(r'^accounts/profile/[\w\d\.]+/change_password/$',views.change_pass),
                       url(r'^accounts/profile/([\w\d\.]+)/$',views.profile_view),
    # Examples:
    # url(r'^$', 'django_sandbox.views.home', name='home'),
    # url(r'^django_sandbox/', include('django_sandbox.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls),),
)
