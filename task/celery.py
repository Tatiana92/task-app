from __future__ import absolute_import

from django.conf import settings  # noqa
from django.http import HttpResponse

import xlsxwriter
import StringIO
import datetime
import os
from celery import Celery

from clients.models import Persons

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task.settings')


app = Celery('task')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
    
@app.task
def make_excel():
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
    output = StringIO.StringIO()
    w_book = xlsxwriter.Workbook(output, {'in_memory': True})
    w_sheet = w_book.add_worksheet(Persons._meta.verbose_name)
    head_format = w_book.add_format({'underline': 1, 'border': 2})
    length = []
    i = 0
    for fld in field_list.keys():
        w_sheet.write(0, i, field_list[fld], head_format)
        length.append(len(field_list[fld]))
        for j in range(len(client_list)):
            w_sheet.write(j + 1, i, client_list[j][fld])
            if len(unicode(client_list[j][fld])) > length[i]:
                length[i] = len(unicode(client_list[j][fld]))
        i = i + 1

    i = 0
    for i in range(len(field_list.keys())):
        w_sheet.set_column(i, i, length[i] + 2)
    w_book.close()
    output.seek(0)
    file_name = 'persons.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=" + file_name

    return response