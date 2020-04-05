from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

#import ipdb
#ipdb.set_trace()
urlpatterns = [
#    url(r'^$', views.timemanagerdev, name='timemanagerdev'),
    url(r'^$', views.awelcome, name='awelcome'),
    url(r'adocsearch/$', views.adocsearch, name='adocsearch'),
    url('adocsearchcontent/$', views.adocsearchcontent, name='adocsearchcontent'),
    url(r'adocadd/$', views.adocadd, name='adocadd'),
    url(r'^acustomerorderform/(?P<pk>[0-9]+)/$', views.acustomerorderform, name='acustomerorderform'),
    url(r'^adoc/(?P<pk>[0-9]+)/$', views.adocselector, name='adocselector'),
    url(r'adocremove/(?P<pk>[0-9]+)/$', views.adocremove, name='adocremove'),
    url('acustomerordernewrowadd/$', views.acustomerordernewrowadd, name='acustomerordernewrowadd'),
    url(r'^acustomerordernewrow/(?P<pkdocid>[0-9]+)/(?P<pkproductid>[0-9]+)/(?P<pkdocdetailsid>[0-9]+)/(?P<nextfirstnumonhtml>[0-9]+)/(?P<nextsecondnumonhtml>[0-9]+)/(?P<nextthirdnumonhtml>[0-9]+)/(?P<nextfourthnumonhtml>[0-9]+)/$',
        views.acustomerordernewrow, name='acustomerordernewrow'),
    url(r'^acustomerorderrowremove/(?P<pk>[0-9]+)/$', views.acustomerorderrowremove, name='acustomerorderrowremove'),
    url(r'aorderprocess/$', views.aorderprocess, name='aorderprocess'),
    url(r'adocorderadd/$', views.adocorderadd, name='adocorderadd'),

]
