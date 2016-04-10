
# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm


class Persons(models.Model):
    first_name = models.CharField(max_length=200, verbose_name=u'Имя')
    last_name = models.CharField(max_length=200, verbose_name=u'Фамилия')
    date_of_birth = models.DateField(verbose_name=u'Дата рождения')
    photo = models.CharField(max_length=200, verbose_name=u'Фото')
    votes = models.IntegerField(default=0, verbose_name=u'Рейтинг')
    age = models.IntegerField(default=0, verbose_name=u'Возраст')



#-----------------------------------------------------
class PersonsForm(ModelForm):
    class Meta:
        model = Persons


