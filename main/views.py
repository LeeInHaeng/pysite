from django.http import HttpResponse
from django.shortcuts import render
import json


def index(request):
    return render(request, 'main/index.html')


def test(request):
    if request.method == 'POST':
        print('post')
        text_input = request.POST['text_input']
        print(text_input)
        return render(request, 'main/index.html')
    else:
        print('get')
        text_input = request.GET['text_input']
        print(text_input)
        return render(request, 'main/index.html')


def ajaxtest(request):
    if request.method == 'POST':
        ajax_data = json.loads(request.body.decode(encoding='utf-8'))
        print(ajax_data)
        ajax_data['data1'] = ajax_data['data1'] + '_success'
        ajax_data['data2'] = ajax_data['data2'] + '_success'
        ajax_data['data3'] = ajax_data['data3'] + '_success'
    return HttpResponse(json.dumps(ajax_data), content_type="application/json")