from django.shortcuts import render

# Create your views here.
def allRooms (request):
   return render(request, 'rooms.html')

