import math

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Max, F, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render

from board.models import Board
from user.models import User


def list(request):
    search = request.GET.get('search', '')
    page = request.GET.get('page', '')
    board_list_all = Board.objects.filter(
        Q(title__contains=search) |
        Q(content__contains=search)).order_by('-groupno', 'orderno')

    page_size = 5
    paginator = Paginator(board_list_all, page_size)

    try:
        if int(page) < 1:  page = 1
        if int(page) > paginator.num_pages:  page = paginator.num_pages
        board_list_page = paginator.page(page)
    except ValueError:
        page = 1
        board_list_page = paginator.page(page)
    page_range_size = 3
    page_range_begin = (math.floor((int(page) - 1) / page_range_size) * page_range_size) + 1
    page_range_end = page_range_begin + page_range_size - 1
    page_range = tuple(range(page_range_begin, page_range_end+1))

    data = {
        'board_list': board_list_page,
        'page_range': page_range
    }
    return render(request, 'board/list.html', data)


def write(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']

        if title == '' or content == '':
            data = {
                'result': 'fail',
                'message': '제목과 내용을 입력해 주세요',
                'title': title,
                'content': content,
            }
            return render(request, 'board/write.html', data)

        board = Board()
        board.title = title
        board.content = content

        max_groupno = Board.objects.aggregate(max_groupno=Max('groupno'))
        board.groupno = 0 if max_groupno["max_groupno"] is None else max_groupno["max_groupno"]+1

        try:
            board.user = User.objects.get(id=request.session['authuser']['id'])
            board.save()
            return HttpResponseRedirect(f'/board?search={request.GET.get("search", "")}&page={request.GET.get("page", "")}')
        except Exception as e:
            print(e)
            data = {
                'result': 'fail',
                'message': '권한이 없습니다',
                'url': f'/board?search={request.GET.get("search", "")}&page={request.GET.get("page", "")}'
            }
            return render(request, 'main/redirect.html', data)

    else:
        return render(request, 'board/write.html')


def view(request):
    no = request.GET.get('no', -1)

    try:
        board = Board.objects.get(id=no)
        board.hit = board.hit + 1
        board.save()
        data = {
            'board': board
        }
        return render(request, 'board/view.html', data)
    except Exception as e:
        print(e)
        data = {
            'result': 'fail',
            'message': '게시글이 존재하지 않습니다',
            'url': f'/board?search={request.GET.get("search", "")}&page={request.GET.get("page", "")}'
        }
        return render(request, 'main/redirect.html', data)


def modify(request):

    if request.method == 'POST':
        board = Board()

        board.title = request.POST['title']
        board.content = request.POST['content']
        bid = request.POST['bid']

        if board.title == '' or board.content == '':
            data = {
                'result': 'fail',
                'message': '제목과 내용을 입력해 주세요',
                'board': board
            }
            return render(request, 'board/modify.html', data)

        try:
            update_board = Board.objects.get(id=bid)
            update_board.title = board.title
            update_board.content = board.content
            update_board.save()
            return HttpResponseRedirect(f'/board?search={request.GET.get("search", "")}&page={request.GET.get("page", "")}')
        except Exception as e:
            print(e)
            data = {
                'result': 'fail',
                'message': '게시글이 존재하지 않습니다',
                'url': f'/board?search={request.GET.get("search", "")}&page={request.GET.get("page", "")}'
            }
            return render(request, 'main/redirect.html', data)
    else:
        no = request.GET.get('no', -1)

        try:
            board = Board.objects.get(id=no)
            if board.user.id == request.session['authuser']['id']:
                data = {
                    'board': board
                }
                return render(request, 'board/modify.html', data)
            else:
                data = {
                    'result': 'fail',
                    'message': '권한이 없습니다',
                    'url': f'/board/view?no={no}&search={request.GET.get("search", "")}&page={request.GET.get("page", "")}'
                }
                return render(request, 'main/redirect.html', data)
        except Exception as e:
            print(e)
            data = {
                'result': 'fail',
                'message': '게시글이 존재하지 않습니다',
                'url': f'/board?search={request.GET.get("search", "")}&page={request.GET.get("page", "")}'
            }
            return render(request, 'main/redirect.html', data)


def delete(request):
    no = request.GET.get('no', -1)

    try:
        board = Board.objects.get(id=no)

        if board.user.id == request.session['authuser']['id']:
            board.delete()
            return HttpResponseRedirect(f'/board?search={request.GET.get("search", "")}&page={request.GET.get("page", "")}')
        else:
            data = {
                'result': 'fail',
                'message': '권한이 없습니다',
                'url': f'/board?search={request.GET.get("search", "")}&page={request.GET.get("page", "")}'
            }
            return render(request, 'main/redirect.html', data)
    except Exception as e:
        print(e)
        data = {
            'result': 'fail',
            'message': '게시글이 존재하지 않습니다',
            'url': f'/board?search={request.GET.get("search", "")}&page={request.GET.get("page", "")}'
        }
        return render(request, 'main/redirect.html', data)


def reply_write(request):

    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']

        if title == '' or content == '':
            data = {
                'result': 'fail',
                'message': '제목과 내용을 입력해 주세요',
                'title': title,
                'content': content,
            }
            return render(request, 'board/write.html', data)

        no = request.GET.get('no', -1)
        try:
            board = Board.objects.get(id=no)

            try:
                user = User.objects.get(id=request.session['authuser']['id'])

                Board.objects.filter(groupno=board.groupno).filter(orderno__gt=board.orderno).update(orderno=F('orderno')+1)

                reply_board = Board()
                reply_board.title = title
                reply_board.content = content
                reply_board.groupno = board.groupno
                reply_board.orderno = board.orderno + 1
                reply_board.depth = board.depth + 1
                reply_board.user = user
                reply_board.save()

                return HttpResponseRedirect(
                    f'/board?search={request.GET.get("search", "")}&page={request.GET.get("page", "")}')
            except Exception as e:
                print(e)
                data = {
                    'result': 'fail',
                    'message': '권한이 없습니다',
                    'url': f'/board?search={request.GET.get("search", "")}&page={request.GET.get("page", "")}'
                }
                return render(request, 'main/redirect.html', data)

        except Exception as e:
            print(e)
            data = {
                'result': 'fail',
                'message': '게시글이 존재하지 않습니다',
                'url': f'/board?search={request.GET.get("search", "")}&page={request.GET.get("page", "")}'
            }
            return render(request, 'main/redirect.html', data)
    else:
        return render(request, 'board/reply-write.html')