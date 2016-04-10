# -*- coding: utf-8 -*-
import json
import datetime

from django.shortcuts import render
from django.http import HttpResponse

from models import Persons, PersonsForm
from task.settings import MEDIA_URL, MEDIA_ROOT, TASK_PATH
from task.celery import make_excel


def index(request):
    return render(request, 'index.html')

def export_to_xls(request):
    return make_excel.delay().get()

def get_clients(request):
    info_list = Persons.objects.all().values()
    field_list = {}
    client_list = []
    for row in Persons._meta.fields:
        field_list[row.name] = row.verbose_name
    for row in info_list:
        dic = {}
        for i in field_list.keys():
            if type(row[i]) == datetime.date:
                dic[i] = row[i].strftime("%d.%b.%Y")
            else:
                dic[i] = row[i]
        client_list.append(dic)
    context = {'client_list': client_list, 'field_list': field_list}
    return HttpResponse(json.dumps(context), content_type="application/json")


def delete_person(request):
    if request.GET:
        if 'ids' in request.GET:
            delete_ids = request.GET['ids'].split(',');
            Persons.objects.filter(id__in=delete_ids).delete()
            message = 'ok'
        else:
            message = 'error - no ids'
    else:
        message = 'error - no GET values'
    return HttpResponse(message)

def save_person(request):
    import os
    import time
    
    message = '<html><body><textarea>no files</textarea></body></html>'
    if len(request.FILES) != 0:
        response = {}
        upload_image = request.FILES.getlist('file')[0]
        try:
            file_name = '%s' % (str(time.time()).replace('.', '')) + upload_image.name
            destination = open(MEDIA_ROOT + file_name, 'wb+')
            for chunk in upload_image.chunks():
                destination.write(chunk)
            destination.close()
            new_item = Persons()
            new_item.first_name = request.POST['first_name']
            new_item.last_name = request.POST['last_name']
            new_item.date_of_birth = request.POST['date_of_birth']
            new_item.photo = file_name
            new_item.votes = request.POST['votes']
            new_item.age = request.POST['age']
            new_item.save()
            message = '<html><body><textarea>ok</textarea></body></html>'
        except Exception, e:
            message = '<html><body><textarea>error: %s</textarea></body></html>' % (str(e))
        return HttpResponse(message)
    return HttpResponse(message)


def set_vote(request):
    from django.db.models import F

    person_id = request.GET['id']
    vote = int(request.GET['value'])
    pers = Persons.objects.get(id=person_id)
    if pers.votes + vote <= 10:
        pers.votes = F('votes') + vote
        pers.save()
    
    pers = Persons.objects.get(id=person_id)
    return HttpResponse(pers.votes) 

def get_vote_template(request):
    from django.template import Context, loader

    info_list = Persons.objects.all().values('photo', 'votes', 'last_name', 'first_name','id')
    context = {'persons': info_list}
    return render(request, 'voting.html', context)
