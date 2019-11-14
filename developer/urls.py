from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

#import ipdb
#ipdb.set_trace()
urlpatterns = [
    url(r'^$', views.timemanager, name='timemanager'),
    url(r'timemanager/$', views.timemanager, name='timemanager'),
    url('timemanagersearchcontent$', views.timemanagersearchcontent, name='timemanagersearchcontent'),
    url('timemanagerupdateprojectselect$', views.timemanagerupdateprojectselect, name='timemanagerupdateprojectselect'),
    url('timemanagerupdateuserselect$', views.timemanagerupdateuserselect, name='timemanagerupdateuserselect'),
    url('timemanagerupdateissueselect$', views.timemanagerupdateissueselect, name='timemanagerupdateissueselect'),
    url('timemanagerfieldupdate$', views.timemanagerfieldupdate, name='timemanagerfieldupdate'),
    url('timemanageruploadtoits$', views.timemanageruploadtoits, name='timemanageruploadtoits'),
    url('filtertemplatehtmlontimemanagerform$', views.filtertemplatehtmlontimemanagerform,name='filtertemplatehtmlontimemanagerform'),

]