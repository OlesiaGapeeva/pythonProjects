from django.shortcuts import render
from datetime import date

def hello(request):
    return render(request, 'index.html', { 'data' : {
        'current_date': date.today(),
        'list': ['python', 'django', 'html']
    }})

def GetOrders(request):
    return render(request, 'orders.html', {'data' : {
        'current_date': date.today(),
        'orders': [
            {'title': 'Копирайтер', 'salary': 50000, 'company': 'Копи-копи', 'city': 'Москва', 'exp': 'Без опыта', 'image': "https://w7.pngwing.com/pngs/299/589/png-transparent-social-media-computer-icons-technical-computer-network-text-computer.png", 'id': 1},
            {'title': 'Менеджер блогера', 'salary': 10000, 'company': 'Co_blog', 'city': 'Москва','exp': 'Без опыта','image' :None,'id': 2},
            {'title': 'Куратор', 'salary': 7000, 'company': 'Вебскул', 'city': 'Без города','exp': 'Без опыта', 'id': 3},
        ]
    }})

def GetOrder(request, id):
    return render(request, 'order.html', {'data' : {
        'current_date': date.today(),
        'id': id
    }})

def sendText(request):
    input_text = request.POST['text']
    return render(request, 'index.html')