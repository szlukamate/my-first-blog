from django.conf.urls import url
from . import views
#import ipdb
#ipdb.set_trace()
urlpatterns = [
    url(r'^$', views.welcome, name='welcome'),
    url(r'^doc/(?P<pk>[0-9]+)/$', views.docform, name='docform'),
    url(r'^docsearch/$', views.docsearch, name='docsearch'),
    url(r'^quotationrowedit/(?P<pk>[0-9]+)/$', views.quotationrowedit, name='quotationrowedit'),
    ]
