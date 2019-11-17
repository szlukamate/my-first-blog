from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

#import ipdb
#ipdb.set_trace()
urlpatterns = [
    url(r'^$', views.timemanagerdev, name='timemanagerdev'),
    url(r'timemanagerdev/$', views.timemanagerdev, name='timemanagerdev'),
    url('timemanagerdevsearchcontent$', views.timemanagerdevsearchcontent, name='timemanagerdevsearchcontent'),
    url('timemanagerdevupdateprojectselect$', views.timemanagerdevupdateprojectselect, name='timemanagerdevupdateprojectselect'),
    url('timemanagerdevupdateuserselect$', views.timemanagerdevupdateuserselect, name='timemanagerdevupdateuserselect'),
    url('timemanagerdevupdateissueselect$', views.timemanagerdevupdateissueselect, name='timemanagerdevupdateissueselect'),
    url('timemanagerdevfieldupdate$', views.timemanagerdevfieldupdate, name='timemanagerdevfieldupdate'),
    url('timemanagerdevuploadtoits$', views.timemanagerdevuploadtoits, name='timemanagerdevuploadtoits'),
    url('filtertemplatehtmlontimemanagerdevform$', views.filtertemplatehtmlontimemanagerdevform, name='filtertemplatehtmlontimemanagerdevform'),
    url('timemanagerdevupdateissueselectafterchangeprojectselect$', views.timemanagerdevupdateissueselectafterchangeprojectselect, name='timemanagerdevupdateissueselectafterchangeprojectselect'),
    url('timemanagerdevrowenabledformanager$', views.timemanagerdevrowenabledformanager, name='timemanagerdevrowenabledformanager'),

]