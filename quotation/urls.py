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
    url('productlistpricefieldupdate', views.productlistpricefieldupdate, name='productlistpricefieldupdate'),
    url('companyuniversalselections', views.companyuniversalselections, name='companyuniversalselections'),
    url(r'coredata_prefaceforquotation/$', views.coredata_prefaceforquotation, name='coredata_prefaceforquotation'),
    url(r'coredata_prefaceforquotationadd/$', views.coredata_prefaceforquotationadd, name='coredata_prefaceforquotationadd'),
    url(r'coredata_prefaceforquotationremove/(?P<pk>[0-9]+)/$', views.coredata_prefaceforquotationremove, name='coredata_prefaceforquotationremove'),
    url('quotationuniversalselections', views.quotationuniversalselections, name='quotationuniversalselections'),
    url('quotationbackpage', views.quotationbackpage, name='quotationbackpage'),
    url(r'coredata_backpageforquotation/$', views.coredata_backpageforquotation, name='coredata_backpageforquotation'),
    url(r'coredata_backpageforquotationadd/$', views.coredata_backpageforquotationadd, name='coredata_backpageforquotationadd'),
    url(r'coredata_backpageforquotationremove/(?P<pk>[0-9]+)/$', views.coredata_backpageforquotationremove, name='coredata_backpageforquotationremove'),
    url(r'coredata_payment/$', views.coredata_payment, name='coredata_payment'),
    url(r'coredata_paymentadd/$', views.coredata_paymentadd, name='coredata_paymentadd'),
    url(r'coredata_paymentremove/(?P<pk>[0-9]+)/$', views.coredata_paymentremove, name='coredata_paymentremove'),
    url(r'coredata_currency/$', views.coredata_currency, name='coredata_currency'),
    url(r'coredata_currencyadd/$', views.coredata_currencyadd, name='coredata_currencyadd'),
    url(r'coredata_currencyremove/(?P<pk>[0-9]+)/$', views.coredata_currencyremove, name='coredata_currencyremove'),
    url(r'^doclinkfix/(?P<docid>[0-9]+)/(?P<fixstate>[0-9]+)/$', views.doclinkfix, name='doclinkfix'),
    url(r'^doclink/(?P<docid>[0-9]+)/$', views.doclink, name='doclink'),
    url(r'^jobnumberform/(?P<pk>[0-9]+)/$', views.jobnumberform, name='jobnumberform'),
    url(r'^accountentryform/(?P<pk>[0-9]+)/$', views.accountentryform, name='accountentryform'),
    url('accountentryuniversalselections', views.accountentryuniversalselections, name='accountentryuniversalselections'),
    url(r'^accountincomestatement/$', views.accountincomestatement, name='accountincomestatement'),
    url(r'^quotationviewpdf/(?P<docid>[0-9]+)/$', views.quotationviewpdf, name='quotationviewpdf'),
    url(r'^quotationemail/(?P<docid>[0-9]+)/$', views.quotationemail, name='quotationemail'),
    url(r'^emailadd/(?P<pk>[0-9]+)/$', views.emailadd, name='emailadd'),
    url(r'^emailform/(?P<pk>[0-9]+)/$', views.emailform, name='emailform'),

]
