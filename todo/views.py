from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.db import IntegrityError


def home(request):
    return render(request , 'todo/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render ( request , 'todo/signupuser.html' , {'forms': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'] , password=request.POST['password1'])
                user.save()
                login(request , user)
                return redirect(currenttodos)
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'forms': UserCreationForm(),'error':'user name already exist' })
        else:
            return render(request, 'todo/signupuser.html', {'forms': UserCreationForm(), 'error': 'pas doesnt match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html' , {'forms': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user == None:
            return render(request, 'todo/loginuser.html', {'forms': AuthenticationForm(),'error': 'try again' })
        else:
            login(request, user)
            return redirect(currenttodos)

def logoutuser(request):
    logout(request)
    return render(request, 'todo/home.html')



def currenttodos(request):
    return render(request, 'todo/currenttodos.html')

