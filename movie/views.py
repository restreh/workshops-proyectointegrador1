from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    #return HttpResponse('<h1>Welcome to home page</h1>')
    #return render(request,'home.html')
    return render(request,'home.html',{'name':'Juan Restrepo Higuita'})

def about(request):
    return HttpResponse('<h1>About</h1>')