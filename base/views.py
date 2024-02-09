from django.shortcuts import render
from django.http import HttpResponse

rooms = [
    {'id' : '1','name':'Learn Python'},
    {'id' : '2','name':'Spring Boot'},
    {'id' : '3','name':'Learn React'}
]

def home(request):
    context = {'room':rooms}
    return render(request,'base/home.html',context)

def room(request, pk):
    rom = None
    for i in rooms:
        if i['id'] == pk:
            rom = i

    context = {'room':rom}        
    return render(request,'base/room.html',context)  


# Create your views here.
