'''定义learning_logsd的URL模式'''

from django.conf.urls import url
from . import view

urlpatterns = [
	#主页
    path(r'^$',view.index,name='index'),
]