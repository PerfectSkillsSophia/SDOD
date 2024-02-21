import json
from django.shortcuts import render,redirect ,HttpResponseRedirect
from accounts.forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
import random
from django.http import JsonResponse
import string
from sophia import settings
from django.http import JsonResponse
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.data.path.append('nltk_data')
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import cv2
from fer import FER
import math

def FindAcc(S1, S2):
    try:
        X = S1.lower()
        Y = S2.lower()

        S1 = re.split(r'[ ,.!;"()]', X)
        S2 = re.split(r'[ ,.!;"()]', Y)

        S1.sort()
        S2.sort()

        Positive = 0
        Negative = 0

        if len(S1) == 1:
            if S1[0] in S2:
                AccPer = 100
            else:
                AccPer = 0
            return AccPer

        if len(S2) == 1:
            S2.append(".")

        for i in S1:
            if i == "":
                continue

            if i in S2:
                Positive += 1
            else:
                Negative += 1

        Total = Positive + Negative

        AccPer = (Positive * 100) / Total

        if Negative < 5:
            X_list = word_tokenize(X)
            Y_list = word_tokenize(Y)

            sw = stopwords.words("english")
            l1 = []
            l2 = []

            X_set = {w for w in X_list if not w in sw}
            Y_set = {w for w in Y_list if not w in sw}

            rvector = X_set.union(Y_set)
            for w in rvector:
                if w in X_set:
                    l1.append(1)  # create a vector
                else:
                    l1.append(0)
                if w in Y_set:
                    l2.append(1)
                else:
                    l2.append(0)
            c = 0

            for i in range(len(rvector)):
                c += l1[i] * l2[i]
            cosine = c / float((sum(l1) * sum(l2)) ** 0.5)

            if min(AccPer, (cosine * 100)) < 40:
                AccPer = min(AccPer, cosine)
            else:
                AccPer = max(AccPer, cosine)

        return AccPer
    
    except:
        return 0  # or any other value that indicates an error

import requests

API_KEY = "623cfea0aba24d8f981195bbc20d48e0"

def upload_and_transcribe_audio(video_file_path):
    filename = video_file_path
    transcript = ""
    try:
        def read_file(filename, chunk_size=5242880):
            with open(filename, 'rb') as _file:
                while True:
                    data = _file.read(chunk_size)
                    if not data:
                        break
                    yield data

        headers = {'authorization': API_KEY}
        
        # Upload the audio file
        with open(video_file_path, 'rb') as vf:
            response = requests.post('https://api.assemblyai.com/v2/upload', headers=headers, data=read_file(filename))
        json_str1 = response.json()

        # Create a transcription job
        endpoint = "https://api.assemblyai.com/v2/transcript"
        json_data = {
            "audio_url": json_str1["upload_url"]
        }
        response = requests.post(endpoint, json=json_data, headers=headers)
        json_str2 = response.json()

        # Get the transcript
        endpoint = "https://api.assemblyai.com/v2/transcript/" + json_str2["id"]
        response = requests.get(endpoint, headers=headers)
        json_str3 = response.json()

        while json_str3["status"] != "completed":
            response = requests.get(endpoint, headers=headers)
            json_str3 = response.json()
        
        transcript = json_str3["text"]
    except Exception as e:
        print(f"An error occurred: {e}")

    return transcript




def analyze_video_emotions(video_filename):
    vid = cv2.VideoCapture(video_filename)
    fps = int(vid.get(cv2.CAP_PROP_FPS) / 3)  # Process every third frame
    emotion_detector = FER()
    n = 0
    i = 0
    sad1 = fear1 = happy1 = angry1 = surprise1 = disgust1 = neutral1 = 0

    while True:
        ret, frame = vid.read()
        if not ret:
            break
        if n % fps == 0:
            attri = emotion_detector.detect_emotions(frame)
            print(attri)
            if len(attri) > 0:
                sad1 += attri[0]["emotions"]['sad']
                fear1 += attri[0]["emotions"]['fear']
                happy1 += attri[0]["emotions"]['happy']
                angry1 += attri[0]["emotions"]['angry']
                surprise1 += attri[0]["emotions"]['surprise']
                disgust1 += attri[0]["emotions"]['disgust']
                neutral1 += attri[0]["emotions"]['neutral']
                i += 1
        n += 1
    vid.release()

    total = sad1 + fear1 + happy1 + angry1 + surprise1 + disgust1 + neutral1
    
    if total == 0:
        confidence = 0
        nervousness = 0
    else:
        confidence = ((happy1 + surprise1) / total) * 100
        nervousness = ((sad1 + fear1 + disgust1) / total) * 100

        if confidence % 1 > 0.4:
            confidence = math.ceil(confidence)
        else:
            confidence = math.floor(confidence)

        if nervousness % 1 > 0.4:
            nervousness = math.ceil(nervousness)
        else:
            nervousness = math.floor(nervousness)

        neutral1 = 100 - (confidence + nervousness)

    return confidence, nervousness, neutral1


def generate_random_code():
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for i in range(7))
    return code

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
				return redirect('response_evaluation_select')
			else:
				messages.warning(request, 'Incorrect Credentials ')

		context = {}
		return render(request, 'response_evaluation_login.html', context)




	
def response_evaluation_select(request):
	return render(request, 'select.html')


def re_result_view(request, test_code):
    url = settings.MEDIA_URL
    all_re = re_recordings.objects.filter(Submission_code=test_code)
    
    try:
        user_test_instance = UserSubmittedTest.objects.get(Submission_code=test_code)
        result_generate = user_test_instance.result_generate
    except UserSubmittedTest.DoesNotExist:
        result_generate = None

    print(test_code)
    return render(request, 'viewre.html', {'re': all_re, 'url': url, 'test_code': test_code, 'result_generate': result_generate})



def response_evaluation_dashboard(request):
	user_assessments = response_evaluation_Assessment.objects.filter(user=request.user)
	submissions = UserSubmittedTest.objects.filter(created_by=request.user)	
	print(submissions)

	return render(request, 'response_evaluation_dashboard.html',{'user_assessments' : user_assessments,'data':submissions})

def response_evaluation_test_dashboard(request):
	return render(request, 're_test_1stpage.html')


def response_evaluation_result(request, test_code):
    ref_url = request.META.get('HTTP_REFERER')
    recordings = re_recordings.objects.filter(Submission_code=test_code)

    ans_id_video_dict = {recording.id: recording.videoAns.path for recording in recordings}


    for id, video_file in ans_id_video_dict.items():
        result = re_recordings.objects.get(id=id)
        vf = video_file
        confidence, nervousness, neutral = analyze_video_emotions(vf)
        transcript = upload_and_transcribe_audio(vf)
        result.confidence = confidence
        result.nervousness = nervousness
        result.neutral = neutral
        result.transcript = transcript
        # Additional code for accuracy calculation
        s1 = UserSubmittedQuestion.objects.get(question=result.question_id).answer
        s2 = transcript
        acc = FindAcc(s1, s2)
        result.answer_accurecy = acc

        result.save()
        

    user_test_instance = UserSubmittedTest.objects.get(Submission_code=test_code)
    user_test_instance.result_generate = True
    user_test_instance.save()


    return HttpResponseRedirect(ref_url)





def response_evaluation_test (request):
		if request.method == 'POST':
			assessment_code = request.POST.get('identi_assessment')
			assess=response_evaluation_Assessment.objects.get(assessment_code=assessment_code)
			assessment_code = assess.assessment_code
			allque = assess.usersubmittedquestion_set.all()			
			print(allque)
			return render(request, 're_test.html',{'question': allque, 'assessment_code':assessment_code})		
		else:
				return render(request,'assessments_dashboard.html')

def Response_Evaluation_Assessment(request):
	if request.method == 'GET':
		question_params = ['que1', 'que2', 'que3', 'que4', 'que5']
		answer_params = ['correctanswer1', 'correctanswer2', 'correctanswer3', 'correctanswer4', 'correctanswer5']
		random_number = random.choice(string.digits)
		random_character = random.choice(string.ascii_letters)
		identi_assessment = "ResponseEvaluation" + "_" + random_number + random_character
		new_assessment = response_evaluation_Assessment.objects.create(user=request.user, title='Response_Evaluation',assessment_code = identi_assessment )
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




def fileUpload(request):
	if request.method == 'POST':
		username = request.user
		test_code = request.POST.get('test_code').strip()
		cb = response_evaluation_Assessment.objects.get( assessment_code = test_code)
		code = generate_random_code()
		newre= UserSubmittedTest.objects.create(Submitted_user_name= username,test_code = test_code ,Submission_code=code ,created_by = cb.user)
		videos = []
		qid_list = []

		questions = json.loads(request.POST.get('questions'))
		for question in questions:
			qid = question.split()[-1]
			qid_list.append(qid)
			print(qid)
		for i in range(len(request.FILES)):
			video = request.FILES['video_%d' % i]
			videos.append(video)
        # Create a video answer object for each uploaded video
		for i, video in zip(qid_list,videos):

			re_recordings.objects.create(videoAns=video,test=newre,Submission_code=code,question_id=i)
			response_data = {'status': 'success'}
		return JsonResponse(response_data)
	else:
		response_data = {'status': 'error', 'message': 'Invalid request method'}
		return JsonResponse(response_data, status=405)

