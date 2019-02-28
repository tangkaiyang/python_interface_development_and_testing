from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect


# Create your views here.
def index(request):
    # return HttpResponse("Hello Django!")
    return render(request, "index.html")


def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        # 登录动作
        if username == 'admin' and password == 'admin123':
            # return HttpResponse(request.method)
            response = HttpResponseRedirect('/event_manage/')
            # response.set_cookie('user', username, 3600)  # 添加浏览器cookie
            request.session['user'] = username # 将session信息记录到浏览器
            # return HttpResponseRedirect('/event_manage/')
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})


# 发布会管理
def event_manage(request):
    # return render(request, "event_manage.html")
    # username = request.COOKIES.get('user', '')  # 读取浏览器cookie
    username = request.session.get('user', '') # 读取浏览器session
    return render(request, "event_manage.html", {"user": username})
