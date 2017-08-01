# -*- coding:utf-8 -*-
import leancloud
from django.shortcuts import render

# Create your views here.
from leancloud import Query, LeanCloudError

from LCD.models import Todo

TRASHED, PLANNED, COMPLETED = -1, 0, 1


def home(request):
    string = u"我在自强学堂学习Django，用它来建网站"
    return render(request, 'home.html', {'string': string})


def show(request):
    try:
        todo = Query(Todo).descending('createdAt').find()
        todo = [x.get('content') for x in todo]
    except LeanCloudError as e:
        todo = []
        raise e
    return render(request, 'todos.html', {'todos': todo})
