from django.forms import model_to_dict
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
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
        user = User.objects.get(email=email)
    except Exception as e:
        user = None
    result = {
        'result': 'success',
        'data': 'exist' if user is None else 'not exist'
    }

    # try:
    #     check_email = User.objects.get(email=email)
    #     data = {'data': check_email.email }
    #     return HttpResponse(json.dumps(data), content_type="application/json")
    # except User.DoesNotExist:
    #     data = {'data': ''}
    #     return HttpResponse(json.dumps(data), content_type="application/json")
    return JsonResponse(result)


def loginform(request):
    return render(request, 'user/loginform.html')


def login(request):
    email = request.POST['email']
    password = request.POST['password']

    results = User.objects.filter(email=email) \
                .filter(password=password)

    if len(results) == 0:
        return HttpResponseRedirect('/user/loginform?result=fail')

    authuser = results[0]
    request.session['authuser'] = model_to_dict(authuser)
    return HttpResponseRedirect('/board')
    # try:
    #     user_data = User.objects.get(email=email, password=password)
    #     request.session['auth_user_email'] = user_data.email
    #     request.session['auth_user_name'] = user_data.name
    #     return render(request, 'main/index.html')
    # except User.DoesNotExist:
    #     return render(request, 'user/loginform.html', {'result': 'fail'})


def logout(request):
    del request.session['authuser']
    return HttpResponseRedirect('/')


def updateform(request):
    user = User.objects.get(id=request.session['authuser']['id'])
    data = {
        'user': user
    }
    return render(request, 'user/updateform.html', data)


def update(request):
    user = User.objects.get(id=request.session['authuser']['id'])
    user.name = request.POST['name']
    user.gender = request.POST['gender']
    if request.POST['password'] is not '':
        user.password = request.POST['password']
    user.save()
    # request.session['authuser'] = model_to_dict(user)
    request.session['authuser']['name'] = user.name
    return HttpResponseRedirect('/')