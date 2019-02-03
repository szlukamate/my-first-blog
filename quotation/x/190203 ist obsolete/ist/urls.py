from django.conf.urls import url
from . import views
#import ipdb
#ipdb.set_trace()
urlpatterns = [
    url(r'^$', views.welcome, name='welcome'),
   # url(r'issues/$', views.issues, name='issues'),

]
