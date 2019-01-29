from django.conf.urls import url
from . import views
#import ipdb
#ipdb.set_trace()
urlpatterns = [
    url(r'^$', views.welcome, name='welcome'),
    url(r'^doc/(?P<pk>[0-9]+)/$', views.docselector, name='docselector'),
    url(r'docadd/$', views.docadd, name='docadd'),
    url(r'docremove/(?P<pk>[0-9]+)/$', views.docremove, name='docremove'),
    url(r'^quotationform/(?P<pk>[0-9]+)/$', views.quotationform, name='quotationform'),
    url(r'^quotationprint/(?P<docid>[0-9]+)/$', views.quotationprint, name='quotationprint'),
    url(r'^orderform/(?P<pk>[0-9]+)/$', views.orderform, name='orderform'),
    url(r'docs/$', views.docs, name='docs'),
    url(r'^companies/$', views.companies, name='companies'),
    url(r'^products/(?P<pkproductid>[0-9]+)/$', views.products, name='products'),
    url(r'^companynew/$', views.companynew, name='companynew'),
    url(r'^companyremove/(?P<pk>[0-9]+)/$', views.companyremove, name='companyremove'),
    url(r'companyedit/(?P<pk>[0-9]+)/$', views.companyedit, name='companyedit'),
    url(r'^quotationnewrow/(?P<pkdocid>[0-9]+)/(?P<pkproductid>[0-9]+)/(?P<pkdocdetailsid>[0-9]+)/(?P<nextfirstnumonhtml>[0-9]+)/(?P<nextsecondnumonhtml>[0-9]+)/(?P<nextthirdnumonhtml>[0-9]+)/(?P<nextfourthnumonhtml>[0-9]+)/$', views.quotationnewrow, name='quotationnewrow'),
    url('quotationnewrowadd', views.quotationnewrowadd, name='quotationnewrowadd'),
    url(r'^quotationupdatecontact/(?P<pkdocid>[0-9]+)/(?P<pkcontactid>[0-9]+)/$', views.quotationupdatecontact, name='quotationupdatecontact'),
    url('productupdatecurrencyisocode', views.productupdatecurrencyisocode, name='productupdatecurrencyisocode'),
    url(r'^productnew/$', views.productnew, name='productnew'),
    url(r'^productremove/(?P<pkproductid>[0-9]+)/$', views.productremove, name='productremove'),
    url(r'^quotationrowremove/(?P<pk>[0-9]+)/$', views.quotationrowremove, name='quotationrowremove'),
    url('searchquotationcontacts', views.searchquotationcontacts, name='searchquotationcontacts'),
    url('productsalespricefieldupdate', views.productsalespricefieldupdate, name='productsalespricefieldupdate'),

]
