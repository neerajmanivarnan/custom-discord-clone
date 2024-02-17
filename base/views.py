from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Room,Topic
from .forms import RoomForm
from django.db.models import Q
from django.contrib import messages

# rooms = [
#     {'id' : '1','name':'Learn Python'},
#     {'id' : '2','name':'Spring Boot'},
#     {'id' : '3','name':'Learn React'}
# ]


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User not found')
    context={}
    return render(request,'base/login_reg.html',context)

def home(request):
    count =0
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # rooms = Room.objects.filter(topic__name__icontains=q)
    rooms = Room.objects.filter(Q(topic__name__icontains=q) |
        Q(name__icontains=q) | 
        Q(description__icontains=q)
    
    )
    count = rooms.count()
    

    # rooms = Room.objects.all()
    topic  = Topic.objects.all()
    
    context = {'room':rooms,'topics':topic,'room_count':count}
    return render(request,'base/home.html',context)

def room(request, pk):
    rooms = Room.objects.get(id=pk)
    # rom = None
    # for i in rooms:
    #     if i['id'] == pk:
    #         rom = i

    context = {'room':rooms}        
    return render(request,'base/room.html',context)  

def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request,'base/room_form.html',context)


def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request,'base/room_form.html',context)


def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    else:
        return render(request,'base/delete.html',{'obj':room})