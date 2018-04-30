'''定义learning_logsd的URL模式'''

from django.conf.urls import url
from . import views

urlpatterns = [
	#主页
    url(r'^$',views.index,name='index'),

    #显示所有主题
    url(r'^topics$', views.topics, name="topics"),
    #特定主题的详细页面
    url(r'^topics/(?P<topic_id>\d+)$', views.topic, name="topic"),
]