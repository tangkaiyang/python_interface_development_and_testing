from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import auth  # 调用Django自带的用户系统
from django.contrib.auth.decorators import login_required  # 调用修饰符
from sign.models import Event, Guest
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.dates import DateFormatter
import matplotlib.pyplot as plt
import PIL

import random
import datetime


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
            request.session['user'] = username  # 将session信息记录到浏览器
            # return HttpResponseRedirect('/event_manage/')
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})


# 发布会管理
# @login_required
def event_manage(request):
    # return render(request, "event_manage.html")
    # username = request.COOKIES.get('user', '')  # 读取浏览器cookie
    # username = request.session.get('user', '') # 读取浏览器session
    # return render(request, "event_manage.html", {"user": username})
    event_list = Event.objects.all()
    username = request.session.get('user', '')
    return render(request, "event_manage.html", {"user": username,
                                                 "events": event_list})


# 发布会名称搜索
# @login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {"user": username,
                                                 "events": event_list})


# 嘉宾管理
# @login_required
def guest_manage(request):
    username = request.session.get("user", '')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    return render(request, "guest_manage.html", {"user": username,
                                                 "guests": contacts})


# 嘉宾姓名搜索
# @login_required
def search_realname(request):
    username = request.session.get('user', '')
    search_realname = request.GET.get("realname", "")
    guest_list = Guest.objects.filter(realname__contains=search_realname)
    return render(request, "guest_manage.html", {"user": username,
                                                 "guests": guest_list})


# 签到页面
# @login_required
def sign_index(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'sign_index.html', {'event': event})


# 签到动作
# @login_required
def sign_index_action(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    phone = request.POST.get('phone', '')

    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'phone error.'})

    result = Guest.objects.filter(phone=phone, event_id=event_id)
    if not result:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'event id or phone error.'})

    result = Guest.objects.get(phone=phone, event_id=event_id)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'user has sign in.'})
    else:
        Guest.objects.filter(phone=phone, event_id=event_id).update(sign='1')
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'sign in success!',
                                                   'guest': result})

# 退出登录
@login_required
def logout(request):
    auth.logout(request)  # 退出登录
    response = HttpResponseRedirect('/index/')
    return response


# def gen_mat(request):
#     fig = plt.figure()
#
#     plt.rcParams['font.sans-serif'] = ['SimHei']
#     plt.rcParams['axes.unicode_minus'] = False
#
#     data = {'丰田': 1, '丰田雷凌': 3, '别克英朗': 2, '北汽EU5': 29, '北汽EX360': 48, '北汽EX360 ': 1, '北汽Eu5': 1, '北汽eu5': 1,
#             '吉利EV450': 1,
#             '大众宝来': 59, '尼桑天籁': 16, '尼桑蓝鸟': 6, '尼桑轩逸': 129, '斯柯达速派': 46, '日产蓝鸟': 1, '日产轩逸': 4, '比亚迪秦': 1, '蓝鸟': 1,
#             '轩逸': 2,
#             '长安欧尚': 2, '雷凌双擎': 2, '雷凌双擎丰田': 1}
#     x = data.keys()
#     y = data.values()
#     # 柱状图
#     plt.subplot(111)
#     plt.xlabel("汽车品牌")
#     plt.ylabel("数量/辆")
#     plt.xticks(size=8)
#     fig.autofmt_xdate() # x轴刻度倾斜
#     plt.bar(x, y)
#     canvas = FigureCanvasAgg(fig)
#     response = HttpResponse(content_type='image/jpg')
#     canvas.print_jpg(response)
#     plt.close()
#     return response
