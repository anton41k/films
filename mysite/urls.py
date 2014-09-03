# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from film.forms import *
from film.views import *
from django.views.generic import list_detail
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
#from dajaxice.core import dajaxice_autodiscover, dajaxice_config
#dajaxice_autodiscover()
admin.autodiscover()

film_list_info={
		'queryset':Films.objects.all(),
		'paginate_by':2,
		'template_name':'film.html'}

urlpatterns = patterns('',
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
    url(r'^xhr_proc/$', proc),
    url(r'^xhr_test/$', xhr_test),
    url(r'^$',film),
    url(r'^filter/$',film),
    url(r'^search/$',search),
    url(r'^user/(?P<send_pk>\d+)/sms/$', sms),
    url(r'^user/(?P<send_pk>\d+)/sms/(?P<add_film_user_pk>\d+)/(?P<rec_pk>\d+)/$', sms),
    url(r'^user/(?P<send_pk>\d+)/(?P<rec_pk>\d+)/(?P<sms_pk>\d+)/sms/$', sms),
    url(r'^user/sms/$', user_sms),
    url(r'^user/(?P<user_pk>\d+)/coments/$', coments_user),
    url(r'^user/sms_sends/$', sms_sends),
    url(r'^user/(?P<i_pk>\d+)/send_sms/$', dispatch ),
    url(r'^user/(?P<i_pk>\d+)/(?P<u_pk>\d+)/del_sms/$', dispatch ),
    url(r'^(?P<i_pk>\d+)/$', detail),
    url(r'^(?P<i_pk>\d+)/coment/$', coments),
    url(r'^(?P<i_pk>\d+)/(?P<com_pk>\d+)/del_coment/$', coments),
    url(r'^(?P<i_pk>\d+)/(?P<coment_pk>\d+)/$', coments),
    url(r'^user/(?P<i_pk>\d+)/new_sms/$', new_sms),
    url(r'^user/(?P<i_pk>\d+)/(?P<u_pk>\d+)/new_sms/$', new_sms),
    url(r'^user/(?P<i_pk>\d+)/$', users),
    url(r'^user/add/$', adduser),
    url(r'^genre/(?P<genre_pk>\d+)/$', film),
    url(r'^addfilm/$', add_film),
    url(r'^addfilm/(?P<film_pk>\d+)/$', add_film),
    url(r'^del_add_film/(?P<add_film_pk>\d+)/$', del_add_film),
    url(r'^new/movies/check/$', new_movies_to_check),
    url(r'^movies/check/$', movies_to_check),
    url(r'^advanced_search/$', advanced_search),
    url(r'^register/$', register),
    url( r'^logout/$', log_out),
    url(r'^admin/', include(admin.site.urls)),
    #url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)


