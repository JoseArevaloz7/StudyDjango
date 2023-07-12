from django.shortcuts import render
from .models import Room

rooms = [
    {'id': 1, 'name': 'Lets learn python!'},
    {'id': 2, 'name': 'Desing with me'},
    {'id': 3, 'name': 'Frontend developers'},
]


# Create your views here.
def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request=request, template_name='base/home.html', context=context)

def room(request, pk):
    room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i
    context = {'room': room}
    return render(request=request, template_name='base/room.html', context=context)

def createRoom(request):
    context = {}
    return render(request=request, template_name='base/room_form.html', context=context)