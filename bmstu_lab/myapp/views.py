from django.shortcuts import render
from datetime import date
from myapp.models import *

def GetVacancies(request):
    keyword = request.GET.get('keyword')
    a = Vacancies.objects.filter(status='enabled')
    if keyword:
         keyword = keyword[0].upper()+keyword[1:]
         a = Vacancies.objects.filter(status='enabled').filter(title=keyword)
    return render(request, 'vacancies.html', {'data': {
        'current_date': date.today(),
        'vacancies': a},
        "search_query": keyword if keyword else ""})

def GetVacancy(request, id):
    return render(request, 'vacancy.html', {'data' : {
        'current_date': date.today(),
        'vacancy': Vacancies.objects.get(id = id)
    }})


# Create your views here.
