from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import auth  # 调用Django自带的用户系统
from django.contrib.auth.decorators import login_required  # 调用修饰符


# Create your views here.
def index(request):
    # return HttpResponse("Hello Django!")
    return render(request, "index.html")


def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        # 登录动作
        if user is not None:
            auth.login(request, user)
        # if username == 'admin' and password == 'admin123':
            # return HttpResponse(request.method)
            response = HttpResponseRedirect('/event_manage/')
            # response.set_cookie('user', username, 3600)  # 添加浏览器cookie
            request.session['user'] = username # 将session信息记录到浏览器
            # return HttpResponseRedirect('/event_manage/')
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})


# 发布会管理
@login_required
def event_manage(request):
    # return render(request, "event_manage.html")
    # username = request.COOKIES.get('user', '')  # 读取浏览器cookie
    username = request.session.get('user', '') # 读取浏览器session
    return render(request, "event_manage.html", {"user": username})