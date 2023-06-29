from django.shortcuts import render,redirect
from accounts.forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def home (request):
	if request.user.is_authenticated:
		if request.user.is_staff:
			return redirect('dashboard')
		return redirect('afterlogin')
	else:
		return render(request,'index.html')

def registerPage(request):
	if request.user.is_authenticated:
		if request.user.is_staff:
			return redirect('dashboard')
		return redirect('welcome')
	else:
		form = UserRegistrationForm()
		if request.method == 'POST':
			form = UserRegistrationForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account Created successfully'+'' + 'Hello'+'' + user)

				return redirect('login')
			

		context = {'form':form}
		return render(request, 'register.html', context)
	
def loginPage(request):
	if request.user.is_authenticated:
		if request.user.is_staff:
			return redirect('dashboard')
		return redirect('welcome')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				if request.user.is_staff:
					return redirect('dashboard')
				return redirect('afterlogin')
			else:
				messages.warning(request, 'Incorrect Credentials ')

		context = {}
		return render(request, 'login.html', context)
	
def staffLogin(request):
	if request.user.is_authenticated:
		return redirect('dashboard')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('dashboard')
			else:
				messages.warning(request, 'Incorrect Credentials')

		context = {}
		return render(request, 'stafflogin.html', context)
	
def logoutUser(request):
	logout(request)
	messages.warning(request, 'LogedOut Successfully!')
	return render(request,'index.html')
