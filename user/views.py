from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from user.models import User
import json


def joinform(request):
    return render(request, 'user/joinform.html')


def join(request):
    user = User()

    user.name = request.POST['name']
    user.email = request.POST['email']
    user.password = request.POST['password']
    user.gender = request.POST['gender']

    user.save()

    return HttpResponseRedirect('/user/joinsuccess')


def joinsuccess(request):
    return render(request, 'user/joinsuccess.html')


def checkemail(request):
    email = request.GET['email']

    try:
        check_email = User.objects.get(email=email)
        data = {'data': check_email.email }
        return HttpResponse(json.dumps(data), content_type="application/json")
    except User.DoesNotExist:
        data = {'data': ''}
        return HttpResponse(json.dumps(data), content_type="application/json")


def loginform(request):
    return render(request, 'user/loginform.html')


def login(request):
    email = request.POST['email']
    password = request.POST['password']

    try:
        user_data = User.objects.get(email=email, password=password)
        request.session['auth_user_email'] = user_data.email
        request.session['auth_user_name'] = user_data.name
        return render(request, 'main/index.html')
    except User.DoesNotExist:
        return render(request, 'user/loginform.html', {'result': 'fail'})


def logout(request):
    if request.session['auth_user_email'] and request.session['auth_user_name']:
        del request.session['auth_user_email']
        del request.session['auth_user_name']
    return HttpResponseRedirect('/')