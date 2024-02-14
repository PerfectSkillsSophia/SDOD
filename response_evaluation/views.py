from django.shortcuts import render,redirect
from accounts.forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
import random
import string



def response_evaluation_login(request):
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
				return redirect('response_evaluation_dashboard')
			else:
				messages.warning(request, 'Incorrect Credentials ')

		context = {}
		return render(request, 'response_evaluation_login.html', context)


	
def response_evaluation_dashboard(request):
	user_assessments = response_evaluation_Assessment.objects.filter(user=request.user)
	print(user_assessments)
	return render(request, 'response_evaluation_dashboard.html',{'user_assessments' : user_assessments})




def Response_Evaluation_Assessment(request):
	if request.method == 'GET':
		question_params = ['que1', 'que2', 'que3', 'que4', 'que5']
		answer_params = ['correctanswer1', 'correctanswer2', 'correctanswer3', 'correctanswer4', 'correctanswer5']
		random_number = random.choice(string.digits)
		random_character = random.choice(string.ascii_letters)
		identi_assessment = str(request.user) + "_" + random_number + random_character
		new_assessment = response_evaluation_Assessment.objects.create(user=request.user, title=identi_assessment)
		for i in range(5):
			question_text = request.GET.get(question_params[i])
			answer_text = request.GET.get(answer_params[i])
			UserSubmittedQuestion.objects.create(
            question=question_text,
            answer=answer_text,
            assessment=new_assessment
        )
		return redirect('response_evaluation_dashboard')
	return redirect('response_evaluation_dashboard')