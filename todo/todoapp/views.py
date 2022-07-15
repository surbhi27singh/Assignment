from django.shortcuts import render, redirect
from .models import Todo
from .forms import TodoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login as signin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# Create your views here.
@login_required(login_url='login')
def index(request):
	tasks = Todo.objects.all()
	form = TodoForm()
	if request.method == 'POST':
		form = TodoForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('/')
	context = {'tasks': tasks, 'form': form}
	return render(request, 'todo/list.html', context)


@login_required(login_url='login')
def updateTask(request, pk):
	task = Todo.objects.get(id=pk)
	form = TodoForm(instance=task)
	if request.method == "POST":
		form = TodoForm(request.POST, instance=task)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form': form}
	return render(request, 'todo/update_task.html', context)

@login_required(login_url='login')
def deleteTask(request, pk):
	item = Todo.objects.get(id=pk)

	if request.method == "POST":
		item.delete()
		return redirect('/')

	context = {'item': item}
	return render(request, 'todo/delete.html', context)


def login(request):
	if request.method == 'GET':
		form = AuthenticationForm()
		context = {"form": form}
		return render(request, 'login.html', context=context)
	form = AuthenticationForm(data=request.POST)
	if form.is_valid():
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		if user is not None:
			signin(request, user)
			return redirect('/')
		context = {
			"form": form
		}
		return render(request, 'login.html', context=context)


def signup(request):
	if request.method == 'GET':
		form = UserCreationForm()
		context = {"form": form}
		return render(request, 'signup.html', context=context)
	form = UserCreationForm(request.POST)
	print(form)
	context = {"form": form}
	if form.is_valid():
		user = form.save()
		print(user)
		if user is not None:
			return redirect(login)
	return render(request, 'signup.html', context=context)


def signout(request):
	logout(request)
	return redirect('login')
