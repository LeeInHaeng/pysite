from django.http import HttpResponseRedirect
from django.shortcuts import render

from guestbook.models import Guestbook


def list(request):
    guestbook_list = Guestbook.objects.all().order_by('-id')
    data = {
        'guestbook_list': guestbook_list
    }
    return render(request, 'guestbook/list.html', data)


def add(request):
    guestbook = Guestbook()

    guestbook.name = request.POST['name']
    guestbook.password = request.POST['password']
    guestbook.contents = request.POST['contents']

    guestbook.save()

    return HttpResponseRedirect('/guestbook')


def deleteform(request):
    delete_no = request.GET['no']
    data = {
        'delete_no': delete_no
    }
    return render(request, 'guestbook/deleteform.html', data)


def delete(request):
    no = request.POST['no']
    password = request.POST['password']

    try:
        data = Guestbook.objects.get(id=no, password=password)
        data.delete()
    finally:
        return HttpResponseRedirect('/guestbook')