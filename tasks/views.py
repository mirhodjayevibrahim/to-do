from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import TaskForm


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('tasks')

    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tasks')
        else:
            messages.error(request, 'An error occurred during registration.')

    return render(request, 'tasks/register.html', {'form': form})


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('tasks')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('tasks')
        else:
            messages.error(request, 'Username or password is incorrect.')

    return render(request, 'tasks/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def taskList(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/list.html', {'tasks': tasks})


@login_required(login_url='login')
def taskCreate(request):
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('tasks')

    return render(request, 'tasks/form.html', {'form': form})


@login_required(login_url='login')
def taskUpdate(request, pk):
    task = Task.objects.get(id=pk, user=request.user)
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks')

    return render(request, 'tasks/form.html', {'form': form})


@login_required(login_url='login')
def taskDelete(request, pk):
    task = Task.objects.get(id=pk, user=request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

    return render(request, 'tasks/delete.html', {'task': task})
