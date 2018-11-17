from django.conf.urls import url
from . import views
#import ipdb
#ipdb.set_trace()
urlpatterns = [
    url(r'^$', views.welcome, name='welcome'),
    url(r'^doc/(?P<pk>[0-9]+)/$', views.docselector, name='docselector'),
    url(r'^docadd/$', views.docadd, name='docadd'),
    url(r'^quotationform/(?P<pk>[0-9]+)/$', views.quotationform, name='quotationform'),
    url(r'^docsearch/$', views.docsearch, name='docsearch'),
    url(r'^quotationrowedit/(?P<pk>[0-9]+)/$', views.quotationrowedit, name='quotationrowedit'),
    url(r'^quotationnewrow/(?P<pk>[0-9]+)/$', views.quotationnewrow, name='quotationnewrow'),
    url(r'^quotationrowremove/(?P<pk>[0-9]+)/$', views.quotationrowremove, name='quotationrowremove')

]
