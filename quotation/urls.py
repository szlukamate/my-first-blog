from django.conf.urls import url
from . import views
#import ipdb
#ipdb.set_trace()
urlpatterns = [
    url(r'^$', views.welcome, name='welcome'),
    url(r'^doc/(?P<pk>[0-9]+)/$', views.docselector, name='docselector'),
    url(r'docadd/$', views.docadd, name='docadd'),
    url(r'^quotationform/(?P<pk>[0-9]+)/$', views.quotationform, name='quotationform'),
    url(r'^orderform/(?P<pk>[0-9]+)/$', views.orderform, name='orderform'),
    url(r'docs/$', views.docs, name='docs'),
    url(r'^companies/$', views.companies, name='companies'),
    url(r'^products/$', views.products, name='products'),
    url(r'^companynew/$', views.companynew, name='companynew'),
    url(r'^companyremove/(?P<pk>[0-9]+)/$', views.companyremove, name='companyremove'),
    url(r'companyedit/(?P<pk>[0-9]+)/$', views.companyedit, name='companyedit'),
    url(r'^quotationnewrow/(?P<pk>[0-9]+)/$', views.quotationnewrow, name='quotationnewrow'),
<<<<<<< HEAD
    #url(r'^quotationupdatecontact/(?P<pkdocid>[0-9]+)/(?P<pkcontactid>[0-9]+)/$', views.quotationupdatecontact, name='quotationupdatecontact'),
    url(r'^quotationupdatecontact/(?P<pkdocid>[0-9]+)/(?P<pkcontactid>[0-9]+)/$', views.quotationupdatecontact, name='quotationupdatecontact'),

=======
>>>>>>> aab59635ca3ec79857281d64a90704dcd3b4576f
    url(r'^quotationrowremove/(?P<pk>[0-9]+)/$', views.quotationrowremove, name='quotationrowremove'),
    url('searchquotationcontacts', views.searchquotationcontacts, name='searchquotationcontacts'),

]
