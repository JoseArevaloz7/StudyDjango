from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic
from .forms import RoomForm

# rooms = [
#     {'id': 1, 'name': 'Lets learn python!'},
#     {'id': 2, 'name': 'Desing with me'},
#     {'id': 3, 'name': 'Frontend developers'},
# ]


# Create your views here.

def loginPage(request):
    
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request=request, message='User does not exist')
            
        user = authenticate(request=request, username=username, password=password)
        
        if user is not None:
            login(request=request, user=user)
            return redirect('home')
        else:
            messages.error(request=request, message='Username or password does not exist')
    
    context = {'page':page}
    
    return render(request=request, template_name='base/login_register.html', context=context)
 
def logoutUser(request):
    logout(request=request)
    return redirect('home')

def registerUser(request):
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request=request, user=user)
            return redirect('home')
        else:
            messages.error(request, 'An error ocurred during regristation')
        
    
    context = {'form': form}
    return render(request=request, template_name='base/login_register.html', context=context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    rooms = Room.objects.filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q) 
        )
    rooms_count = rooms.count()
    topics = Topic.objects.all()
    
    context = {'rooms': rooms, 'topics': topics, 'rooms_count': rooms_count}
    return render(request=request, template_name='base/home.html', context=context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request=request, template_name='base/room.html', context=context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()  
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request=request, template_name='base/room_form.html', context=context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    if request.user != room.host:
        return HttpResponse('You are not allowed here!') 
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form} 
    return render(request=request, template_name='base/room_form.html', context=context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse('You are not allowed here!') 
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    return render(request=request, template_name='base/delete.html', context={'obj': room})
    