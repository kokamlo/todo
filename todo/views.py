from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TodoForm
from .models import Todo
from django.utils import timezone


def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'forms': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect(currenttodos)
            except IntegrityError:
                return render(request, 'todo/signupuser.html',
                              {'forms': UserCreationForm(), 'error': 'user name already exist'})
        else:
            return render(request, 'todo/signupuser.html', {'forms': UserCreationForm(), 'error': 'pas doesnt match'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'forms': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user == None:
            return render(request, 'todo/loginuser.html', {'forms': AuthenticationForm(), 'error': 'try again'})
        else:
            login(request, user)
            return redirect(currenttodos)


def logoutuser(request):
    logout(request)
    return render(request, 'todo/home.html')


def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'forms': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            ntodo = form.save(commit=False)
            ntodo.user = request.user
            ntodo.save()
            return redirect(currenttodos)
        except:
            return render(request, 'todo/createtodo.html', {'forms': TodoForm(), 'error': 'bad input'})


def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, compeliteddate__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos': todos})


def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect(currenttodos)
        except:
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form, 'error': 'bad info'})


def donedo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.compeliteddate = timezone.now()
        todo.save()
        return redirect(currenttodos)


def deldo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect(currenttodos)
