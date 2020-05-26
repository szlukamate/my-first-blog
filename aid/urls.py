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
    url(r'^acustomeracknowledgementform/(?P<pk>[0-9]+)/$', views.acustomeracknowledgementform, name='acustomeracknowledgementform'),
    url(r'^acustomerordersaveasacknowledgement/(?P<pk>[0-9]+)/$', views.acustomerordersaveasacknowledgement, name='acustomerordersaveasacknowledgement'),
    url(r'acustomerorderemailtry/(?P<docid>[0-9]+)/$', views.acustomerorderemailtry, name='acustomerorderemailtry'),
    url(r'adocmyorderssearch/$', views.adocmyorderssearch, name='adocmyorderssearch'),
    url('adocmyorderssearchcontent/$', views.adocmyorderssearchcontent, name='adocmyorderssearchcontent'),
    url(r'^acustomercartform/(?P<pk>[0-9]+)/$', views.acustomercartform, name='acustomercartform'),
    url(r'acustomercartadditemtocart/$', views.acustomercartadditemtocart, name='acustomercartadditemtocart'),
    url(r'^acustomercartrowremove/(?P<pk>[0-9]+)/$', views.acustomercartrowremove, name='acustomercartrowremove'),
    url(r'acustomercartrefresh/$', views.acustomercartrefresh, name='acustomercartrefresh'),
    url(r'acustomercartincreasingqty/$', views.acustomercartincreasingqty, name='acustomercartincreasingqty'),
    url(r'acustomercartdecreasingqty/$', views.acustomercartdecreasingqty, name='acustomercartdecreasingqty'),
    url(r'acustomercartproductremove/$', views.acustomercartproductremove, name='acustomercartproductremove'),
    url(r'acustomercartpricetagtocarttop/$', views.acustomercartpricetagtocarttop, name='acustomercartpricetagtocarttop'),
    url(r'acustomercartsaveasorder/$', views.acustomercartsaveasorder, name='acustomercartsaveasorder'),
    url(r'acustomerconfirmation/(?P<docid>[0-9]+)/$', views.acustomerconfirmation, name='acustomerconfirmation'),
    url(r'amyprofileform/(?P<pk>[0-9]+)/$', views.amyprofileform, name='amyprofileform'),
    url(r'acustomercartaddinganonymoususerid/$', views.acustomercartaddinganonymoususerid, name='acustomercartaddinganonymoususerid'),
    url(r'aauthenticationsignup/$', views.aauthenticationsignup, name='aauthenticationsignup'),
    url(r'^aauthenticationactivate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.aauthenticationactivate, name='aauthenticationactivate'),
    url(r'aauthenticationcheckuserproperties/$', views.aauthenticationcheckuserproperties, name='aauthenticationcheckuserproperties'),
    url(r'aorderprocesspaypalpayment/$', views.aorderprocesspaypalpayment, name='aorderprocesspaypalpayment'),

]
