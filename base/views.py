from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm

# rooms = [
#     {'id': 1, 'name': 'Lets learn python!'},
#     {'id': 2, 'name': 'Desing with me'},
#     {'id': 3, 'name': 'Frontend developers'},
# ]


# Create your views here.
def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request=request, template_name='base/home.html', context=context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request=request, template_name='base/room.html', context=context)

def createRoom(request):
    form = RoomForm()  
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request=request, template_name='base/room_form.html', context=context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    context = {'form': form}
    return render(request=request, template_name='base/room_form.html', context=context)