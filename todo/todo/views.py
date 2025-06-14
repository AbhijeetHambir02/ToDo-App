from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from todo.models import ToDo
import datetime

def signup(request):
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if username and password and email and cpassword:
            if password != cpassword:
                messages.error(request, 'Passwords do not match. Please try again!')
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                return redirect('/login')

    return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if email and password:
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(request, username=user_obj.username, password=user_obj.password)
                if user_obj:
                    login(request, user_obj)
                    return redirect('/todo')
                else:
                    messages.error(request, 'Invalid username or password. Please try again!')
            except User.DoesNotExist:
                messages.error(request, 'Invalid username or password. Please try again!')

    return render(request, 'signin.html')


def todo(request):
    if request.method == 'POST':
        title = request.POST['title']
        start_date = datetime.datetime.fromisoformat(request.POST['startdate'])
        end_date = datetime.datetime.fromisoformat(request.POST['enddate'])
        todo = ToDo(title=title, start_date=start_date, end_date=end_date, user=request.user)
        todo.save()
        todo_list = ToDo.objects.filter(user=request.user).order_by('-task_date')
        return redirect('/todo', {"todo_list": todo_list})
    todo_list = ToDo.objects.filter(user=request.user).order_by('-task_date')
    return render(request, 'todo.html', {"todo_list": todo_list})


def delete_task(request, id):
    todo = ToDo.objects.get(id=id)
    todo.delete()
    return redirect('/todo')