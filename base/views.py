from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Room,Topic,Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm

# rooms = [
#     {'id' : '1','name':'Learn Python'},
#     {'id' : '2','name':'Spring Boot'},
#     {'id' : '3','name':'Learn React'}
# ]


def logoutUser(request):
    logout(request)
    return redirect('home')


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User not found')

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or password does not exist')        
    context={'page':page}
    return render(request,'base/login_reg.html',context)


def registerUser(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user  = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Oops an error occured while registering user")
    context = {'page':page,'form':form}
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
    room_messages = rooms.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = rooms,
            body = request.POST.get('body')
        )
        # return redirect('room')
    context = {'room':rooms,'room_messages':room_messages,'participants':participants}        
    return render(request,'base/room.html',context)  

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not allowed here")

    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You are not allowed here")
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    else:
        return render(request,'base/delete.html',{'obj':room})