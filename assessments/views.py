# Import required Django modules and models
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from assessments.models import videoAns, Feedback , submission_status
from administration.models import allAssessment , Question
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import random
import string


# Define a view function to render a template after user login
@login_required(login_url='login')
def afterlogin(request):
	return render(request,'assessment_link.html')

# Define a view function to render a welcome screen after user selects an assessment
@login_required(login_url='login')
def welcomeScreen(request, ass_name):
    global slug 
    slug = ass_name
    return render(request, 'welcomscreen.html')

# Define a view function to render assessment questions
@login_required(login_url='login')
def answer(request):
    ass_name = slug
    assname = ass_name
    # Get all questions related to the selected assessment
    allque = allAssessment.objects.get(assessmentName=ass_name).question_set.all()
    return render(request, 'answer3.html', {'question': allque, 'assname': assname})

# Define a view function to handle video file uploads via AJAX call
@csrf_exempt
@login_required(login_url='login')
def fileUpload(request):
    if request.method == 'POST':
        # Get username, assessment name and video blobs from the request
        username = request.user
        assessment_name = request.POST.get('ass_name')
        identi= ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        videos = []
        submission_status.objects.create(user_name=username,assessment_name=assessment_name,identi=identi,submissionstatus=True)


        for i in range(len(request.FILES)):
            video = request.FILES['video_%d' % i]
            videos.append(video)
        questions = json.loads(request.POST.get('questions'))
        # Create a video answer object for each uploaded video
        for i in range(len(videos)):
            question = questions[i]
            qid = question.split()[-1]
            video = videos[i]
            question_instance = Question.objects.get(questionId=int(qid))
            videoAns.objects.create(videoAns=video, user_name=username,question_id=question_instance ,assessment_name=assessment_name,identi=identi)
        # Send a JSON response indicating success
        response_data = {'status': 'success'}
        return JsonResponse(response_data)
    else:
        # Send a JSON response indicating error for non-POST request
        response_data = {'status': 'error', 'message': 'Invalid request method'}
        return JsonResponse(response_data, status=405)

# Define a view function to render a feedback form
@login_required(login_url='login')
def feedback(request):
    if request.method == 'POST':
        # Create a Feedback object with user and feedback type and save to database
        feedback_type = request.POST.get('feedback_type')
        feedback = Feedback(user=request.user, feedback_type=feedback_type)
        feedback.save()
        # Redirect to thank you page
        return redirect('thankyou')

    # Render the feedback form
    return render(request, 'feedback.html')

# Define a view function to render a thank you page after feedback submission
@login_required(login_url='login')
def thankyou(request):
    return render(request, 'thankyou.html')


def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)