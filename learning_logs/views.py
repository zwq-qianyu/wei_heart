from django.shortcuts import render
from learning_logs.models import Topic, Entry
from django.http import HttpResponseRedirect, Http404
#from django.core.urlresolvers import reverse
from django.urls import reverse
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required

def check_topic_owner(request, topic):
	if topic.owner != request.user:
		raise Http404

# Create your views here.
def index(request):
	'''学习笔记的主页'''
	return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
	'''显示所有主题'''
	topics = Topic.objects.filter(owner=request.user).order_by('time_added')
	content = {'topics':topics}
	return render(request,'learning_logs/topics.html',content)

@login_required
def topic(request, topic_id):
	'''显示单个主题及其所有的条目'''
	topic = Topic.objects.get(id=topic_id)
	check_topic_owner(request, topic)
	entries = topic.entry_set.order_by('-date_added')
	content = {'topic':topic, 'entries':entries}
	return render(request,'learning_logs/topic.html',content)

@login_required
def new_topic(request):
	'''添加新主题'''
	if request.method != 'POST':
		#未提交数据，创建一个新表单
		form = TopicForm()
	else:
		#post提交的数据，对数据进行处理
		form = TopicForm(request.POST)
		if form.is_valid():
			new_topic = form.save(commit=False)
			new_topic.owner = request.user
			new_topic.save()
			return HttpResponseRedirect(reverse('topics'))

	content = {'form': form}
	return render(request, 'learning_logs/new_topic.html', content)

@login_required
def new_entry(request, topic_id):
	'''添加新条目'''
	topic = Topic.objects.get(id=topic_id)
	check_topic_owner(request, topic)

	if request.method != 'POST':
		#未提交数据，创建一个新表单
		form = EntryForm()
	else:
		#post提交的数据，对数据进行处理
		form = EntryForm(data = request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.topic = topic
			new_entry.save()
			return HttpResponseRedirect(reverse('topic', args=[topic_id]))

	content = {'topic': topic, 'form': form}
	return render(request, 'learning_logs/new_entry.html', content)

@login_required
def edit_entry(request, entry_id):
	'''编辑条目'''
	entry = Entry.objects.get(id = entry_id)
	topic = entry.topic
	check_topic_owner(request, topic)

	if request.method != 'POST':
		#初次请求时，get
		form = EntryForm(instance = entry)
	else:
		#POST提交数据，对数据进行处理
		form = EntryForm(instance=entry, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('topic', args=[topic.id]))

	content = {'entry':entry, 'topic': topic, 'form':form }
	return render(request, 'learning_logs/edit_entry.html', content)
