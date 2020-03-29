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

]
