from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from datetime import date

services =[
    {'title': 'Подробнее', 'aspect': 'Робототехника',
     'id': 0, 'src': 'https://klass.market/uploadedFiles/eshopimages/big/14108ca0.jpg',
        'text': 'Робототехника',
        'simp':['Представители мировых и российских компаний', 'Диалоги с работодателями',\
                'Возможность найти подходящие курсы по робототехнике', \
                'Интерактивные занятия','Советы по программированию роботов'],
     },

    {'title': 'Подробнее','aspect': 'Искусственный интеллект',
     'id': 1,'src':'https://img.freepik.com/premium-vector/artificial-intelligence-cyborg-technological-brain-on-white-background_185386-676.jpg',
        'text':'Искуственный интеллект',
        'simp':['Информационно-телекоммуникационные технологии и моделирование', 'Современные тенденции в Data Science',\
                'Вводные лекции по ИИ', 'Биомедицинские технологии', 'Примеры использования ИИ в повседневной жизни'] },

    {'title': 'Подробнее','aspect': 'Аддитивное производство',
     'id': 2, 
     'src': 'https://www.stankoff.ru/files/blog/mSRdXzYSIA4bizQgbAvT9sG0m2NfJZTrC3poZLhw-big.jpg', \
        'text': 'Аддитивное производство',
        'simp':['Аддитивные технологии позволяют изготавливать любое изделие послойно на основе компьютерной 3D-модели',\
             'Такой процесс создания объекта также называют выращиванием из-за постепенности его изготовления.'] },
]

def GetServices(request):
    return render(request, 'services.html', {'services': services})


def GetService(request, id):
    for s in services:
        if s['id']==id:
            return render(request, 'service.html',{'s': s})


def GetQuery(request):
    query = request.GET.get('query', '')
    #print("__QUERY__ =", query, type(query))
    new_services = []
    for service in services:
        if query.lower() in service["title"].lower():
            new_services.append(service)

    if len(new_services)>0:
        return render(request, 'services.html',{'services': new_services})
    else:
        return render(request, 'services.html', {'services': services})
