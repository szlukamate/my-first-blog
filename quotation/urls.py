from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

#import ipdb
#ipdb.set_trace()
urlpatterns = [
    url(r'^$', views.welcome, name='welcome'),
    url(r'^doc/(?P<pk>[0-9]+)/$', views.docselector, name='docselector'),
    url(r'docadd/$', views.docadd, name='docadd'),
    url(r'docremove/(?P<pk>[0-9]+)/$', views.docremove, name='docremove'),
    url(r'^quotationform/(?P<pk>[0-9]+)/$', views.quotationform, name='quotationform'),
    url(r'^quotationprint/(?P<docid>[0-9]+)/$', views.quotationprint, name='quotationprint'),
    url(r'docs/$', views.docs, name='docs'),
    url(r'^companies/$', views.companies, name='companies'),
    url(r'^products/(?P<pkproductid>[0-9]+)/$', views.products, name='products'),
    url(r'^companynew/$', views.companynew, name='companynew'),
    url(r'^companyremove/(?P<pk>[0-9]+)/$', views.companyremove, name='companyremove'),
    url(r'companyedit/(?P<pk>[0-9]+)/$', views.companyedit, name='companyedit'),
    url(r'^quotationnewrow/(?P<pkdocid>[0-9]+)/(?P<pkproductid>[0-9]+)/(?P<pkdocdetailsid>[0-9]+)/(?P<nextfirstnumonhtml>[0-9]+)/(?P<nextsecondnumonhtml>[0-9]+)/(?P<nextthirdnumonhtml>[0-9]+)/(?P<nextfourthnumonhtml>[0-9]+)/$', views.quotationnewrow, name='quotationnewrow'),
    url('quotationnewrowadd', views.quotationnewrowadd, name='quotationnewrowadd'),
    url(r'^quotationupdatecontact/(?P<pkdocid>[0-9]+)/(?P<pkcontactid>[0-9]+)/$', views.quotationupdatecontact, name='quotationupdatecontact'),
    url('productupdatecurrencyisocode$', views.productupdatecurrencyisocode, name='productupdatecurrencyisocode'),
    url(r'productnew', views.productnew, name='productnew'),
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
    url(r'^quotationemail/(?P<docid>[0-9]+)/$', views.quotationemail, name='quotationemail'),
    url(r'^emailadd/(?P<pk>[0-9]+)/$', views.emailadd, name='emailadd'),
    url(r'^emailform/(?P<pk>[0-9]+)/$', views.emailform, name='emailform'),
    url(r'^emailviewattachment/(?P<pk>[0-9]+)/$', views.emailviewattachment, name='emailviewattachment'),
    url(r'^quotationsaveasmodern/(?P<pk>[0-9]+)/$', views.quotationsaveasmodern, name='quotationsaveasmodern'),
    url(r'^contactadd/(?P<pk>[0-9]+)/$', views.contactadd, name='contactadd'),
    url('productupdatesupplier', views.productupdatesupplier, name='productupdatesupplier'),
    url(r'^quotationsaveasorder/(?P<pk>[0-9]+)/$', views.quotationsaveasorder, name='quotationsaveasorder'),
    url(r'^customerorderform/(?P<pk>[0-9]+)/$', views.customerorderform, name='customerorderform'),
    url(r'^customerorderprint/(?P<docid>[0-9]+)/$', views.customerorderprint, name='customerorderprint'),
    url('customerordernewrowadd', views.customerordernewrowadd, name='customerordernewrowadd'),
    url(r'^customerorderrowremove/(?P<pk>[0-9]+)/$', views.customerorderrowremove, name='customerorderrowremove'),
    url(r'^emailviewattachmentcandidate/(?P<pdffilename>[^/]+)/$', views.emailviewattachmentcandidate, name='emailviewattachmentcandidate'),
    url(r'docsearch/$', views.docsearch, name='docsearch'),
    url('docsearchcontent', views.docsearchcontent, name='docsearchcontent'),
    url(r'purchaseorderpre/$', views.purchaseorderpre, name='purchaseorderpre'),
    url(r'^purchaseorderform/(?P<pk>[0-9]+)/$', views.purchaseorderform, name='purchaseorderform'),
    url(r'purchaseordermake', views.purchaseordermake, name='purchaseordermake'),
    url(r'^purchaserorderprint/(?P<docid>[0-9]+)/$', views.purchaseorderprint, name='purchaseorderprint'),
    url(r'^purchaseorderemail/(?P<docid>[0-9]+)/$', views.purchaseorderemail, name='purchaseorderemail'),
    url(r'^purchaseorderrowremove/(?P<pk>[0-9]+)/$', views.purchaseorderrowremove, name='purchaseorderrowremove'),
    url('purchaseorderbackpage', views.purchaseorderbackpage, name='purchaseorderbackpage'),
    url('contactsettodefaulttopurchaseorder', views.contactsettodefaulttopurchaseorder, name='contactsettodefaulttopurchaseorder'),
    url(r'pohandlerframe/$', views.pohandlerframe, name='pohandlerframe'),
    url('pohandlerfieldsupdate', views.pohandlerfieldsupdate, name='pohandlerfieldsupdate'),
    url('pohandlersearchresults', views.pohandlersearchresults, name='pohandlersearchresults'),
    url(r'^deliverynoteform/(?P<pk>[0-9]+)/$', views.deliverynoteform, name='deliverynoteform'),
    url('pohandlerrowsourceforarrivaldates', views.pohandlerrowsourceforarrivaldates, name='pohandlerrowsourceforarrivaldates'),
    url('pohandlerreception', views.pohandlerreception, name='pohandlerreception'),
    url(r'^deliverynoteprint/(?P<docid>[0-9]+)/$', views.deliverynoteprint, name='deliverynoteprint'),
    url('deliverynotebackpage', views.deliverynotebackpage, name='deliverynotebackpage'),
    url('pohandlersplit', views.pohandlersplit, name='pohandlersplit'),
    url('deliverynotepre', views.deliverynotepre, name='deliverynotepre'),
    url('searchcustomerordercontacts', views.searchcustomerordercontacts, name='searchcustomerordercontacts'),
    url(r'^customerorderupdatecontact/(?P<pkdocid>[0-9]+)/(?P<pkcontactid>[0-9]+)/$', views.customerorderupdatecontact,name='customerorderupdatecontact'),
    url('deliverynotemake', views.deliverynotemake, name='deliverynotemake'),
    url(r'stockmain/$', views.stockmain, name='stockmain'),
    url(r'^customerinvoicemake/(?P<docid>[0-9]+)/$', views.customerinvoicemake, name='customerinvoicemake'),
    url('stocklabellist', views.stocklabellist, name='stocklabellist'),
    url(r'stocktakingpreform/$', views.stocktakingpreform, name='stocktakingpreform'),
    url('stocknewdocforstocktaking', views.stocknewdocforstocktaking, name='stocknewdocforstocktaking'),
    url('stockcopyfromtimestampforstocktaking', views.stockcopyfromtimestampforstocktaking, name='stockcopyfromtimestampforstocktaking'),
    url('deliverynotenewrowadd', views.deliverynotenewrowadd, name='deliverynotenewrowadd'),
    url(r'^deliverynoterowremove/(?P<pk>[0-9]+)/$', views.deliverynoterowremove, name='deliverynoterowremove'),
    url(r'^deliverynotenewrow/(?P<pkdocid>[0-9]+)/(?P<pkproductid>[0-9]+)/(?P<pkdocdetailsid>[0-9]+)/(?P<nextfirstnumonhtml>[0-9]+)/(?P<nextsecondnumonhtml>[0-9]+)/(?P<nextthirdnumonhtml>[0-9]+)/(?P<nextfourthnumonhtml>[0-9]+)/$',
        views.deliverynotenewrow, name='deliverynotenewrow'),
    url('deliverynotenewlabel', views.deliverynotenewlabel, name='deliverynotenewlabel'),
    url('deliverynoteafternewlabel', views.deliverynoteafternewlabel, name='deliverynoteafternewlabel'),
    url(r'^customerordernewrow/(?P<pkdocid>[0-9]+)/(?P<pkproductid>[0-9]+)/(?P<pkdocdetailsid>[0-9]+)/(?P<nextfirstnumonhtml>[0-9]+)/(?P<nextsecondnumonhtml>[0-9]+)/(?P<nextthirdnumonhtml>[0-9]+)/(?P<nextfourthnumonhtml>[0-9]+)/$',
        views.customerordernewrow, name='customerordernewrow'),
    url(r'^customerinvoiceform/(?P<pk>[0-9]+)/$', views.customerinvoiceform, name='customerinvoiceform'),
    url(r'^customerinvoicerowremove/(?P<pk>[0-9]+)/$', views.customerinvoicerowremove, name='customerinvoicerowremove'),
    url(r'^customerinvoiceprint/(?P<docid>[0-9]+)/$', views.customerinvoiceprint, name='customerinvoiceprint'),
    url('customerinvoicebackpage', views.customerinvoicebackpage, name='customerinvoicebackpage'),
    url('customerinvoicedispatch', views.customerinvoicedispatch, name='customerinvoicedispatch'),
    url('customerinvoicexmlresponsepdfstacking', views.customerinvoicexmlresponsepdfstacking, name='customerinvoicexmlresponsepdfstacking'),
    url(r'^customerinvoiceviewpdf/(?P<pk>[0-9]+)/$', views.customerinvoiceviewpdf, name='customerinvoiceviewpdf'),
    url('customerinvoiceshowpdfbutton', views.customerinvoiceshowpdfbutton, name='customerinvoiceshowpdfbutton'),
    url('quotationissuetrackingsystem$', views.quotationissuetrackingsystem, name='quotationissuetrackingsystem'),
    url('quotationissuetrackingsystemitemstoquotation$', views.quotationissuetrackingsystemitemstoquotation, name='quotationissuetrackingsystemitemstoquotation'),
    url('quotationissuetrackingsystempostitems$', views.quotationissuetrackingsystempostitems, name='quotationissuetrackingsystempostitems'),
    url('quotationissuetrackingsystemsearchcontent$', views.quotationissuetrackingsystemsearchcontent, name='quotationissuetrackingsystemsearchcontent'),
    url('productsearchcontent$', views.productsearchcontent, name='productsearchcontent'),
    url('productfieldupdate$', views.productfieldupdate, name='productfieldupdate'),
    url('filtertemplatehtmlonproductform$', views.filtertemplatehtmlonproductform, name='filtertemplatehtmlonproductform'),
    url('filtertemplatehtmlonquotationtimeentryform$', views.filtertemplatehtmlonquotationtimeentryform, name='filtertemplatehtmlonquotationtimeentryform'),
    url(r'timemanager/$', views.timemanager, name='timemanager'),
    url('filtertemplatehtmlontimemanagerform$', views.filtertemplatehtmlontimemanagerform,name='filtertemplatehtmlontimemanagerform'),
    url('timemanagersearchcontent$', views.timemanagersearchcontent, name='timemanagersearchcontent'),
    url('timemanagerupdateprojectselect$', views.timemanagerupdateprojectselect, name='timemanagerupdateprojectselect'),
    url('timemanagerupdateuserselect$', views.timemanagerupdateuserselect, name='timemanagerupdateuserselect'),
    url('timemanagerupdateissueselect$', views.timemanagerupdateissueselect, name='timemanagerupdateissueselect'),
    url('timemanagerfieldupdate$', views.timemanagerfieldupdate, name='timemanagerfieldupdate'),
    url('timemanageruploadtoits$', views.timemanageruploadtoits, name='timemanageruploadtoits'),

]