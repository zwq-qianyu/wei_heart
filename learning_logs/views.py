from django.shortcuts import render
from learning_logs.models import Topic

# Create your views here.
def index(request):
	'''学习笔记的主页'''
	return render(request, 'learning_logs/index.html')

def topics(request):
	'''显示所有主题'''
	topics = Topic.objects.order_by('time_added')
	content = {'topics':topics}
	return render(request,'learning_logs/topics.html',content)

def topic(request, topic_id):
	'''显示单个主题及其所有的条目'''
	topic = Topic.objects.get(id=topic_id)
	entries = topic.entry_set.order_by('-date_added')
	content = {'topic':topic, 'entries':entries}
	return render(request,'learning_logs/topic.html',content)