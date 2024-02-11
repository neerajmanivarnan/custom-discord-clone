from django.shortcuts import render
from django.http import HttpResponse
from .models import Room

# rooms = [
#     {'id' : '1','name':'Learn Python'},
#     {'id' : '2','name':'Spring Boot'},
#     {'id' : '3','name':'Learn React'}
# ]

def home(request):
    rooms = Room.objects.all()
    context = {'room':rooms}
    return render(request,'base/home.html',context)

def room(request, pk):
    rooms = Room.objects.get(id=pk)
    # rom = None
    # for i in rooms:
    #     if i['id'] == pk:
    #         rom = i

    context = {'room':rooms}        
    return render(request,'base/room.html',context)  


# Create your views here.
