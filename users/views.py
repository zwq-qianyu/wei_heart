from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.forms import UserCreationForm

def logout_view(request):
	'''注销操作'''
	logout(request)
	return HttpResponseRedirect(reverse('index'))

def register(request):
	'''注册'''
	if request.method != 'POST':
		#第一次请求显示空的注册表单
		form = UserCreationForm()
	else:
		#处理填好的表单
		form = UserCreationForm(data = request.POST)

		if form.is_valid():
			new_user = form.save()
			#让用户自动登录，再重定向到主页
			authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
			login(request, authenticated_user)
			return HttpResponseRedirect(reverse('index'))

	content = {'form': form}
	return render(request, 'users/register.html', content)