##########   NEW CODE   ##########

from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from assessments.models import *
from django.contrib import messages
from administration.models import *
from django.urls import reverse
from sophia import settings
from statistics import mean
import random
import string
from .func import *


 ##########   Dashboard View   ##########
@staff_member_required
@login_required(login_url='login')
def dashboard(request):
    # Retrieves all assessment objects
    assessment = allAssessment.objects
    # Retrieves the first 5 videoAns objects
    video = videoAns.objects.all()[:5]
    return render(request, 'dashboard.html', {'assessment': assessment, 'video': video})

 ##########   All Submission View   ##########
@staff_member_required
@login_required(login_url='login')
def allAnswer(request):
    # Retrieves distinct user names, assessment names, and identi values from videoAns objects
    all_data = videoAns.objects.all().values('user_name', 'assessment_name', 'identi').distinct()
    return render(request, 'submmision.html', {'all_data': all_data})

 ##########   Add Assessments template View   ##########
@staff_member_required
@login_required(login_url='login')
def add_assessment(request):
    return render(request, 'add_assessments.html')

 ##########   Add Assessments View   ##########
@staff_member_required
@login_required(login_url='login')
def Add_assessment(request):
    if request.method == 'GET':
        ass_name = request.GET.get('ass_name')
        ass_dec = request.GET.get('ass_dec')
        random_number = random.choice(string.digits)
        random_character = random.choice(string.ascii_letters)
        identi_assessment = ass_name + "_" + random_number + random_character
        new_ass = allAssessment()
        new_ass.assessmentName = ass_name
        new_ass.assessmentDes = ass_dec
        new_ass.identi_assessment = identi_assessment
        new_ass.save()
        return redirect('addassessment')
    return redirect('addassessment')

 ##########   Assessments detsil View   ##########
@staff_member_required
@login_required(login_url='login')
def view_assessments(request, ass_id):
    ass_id = ass_id
    # Retrieves allAssessment objects for the given ass_id
    assessment = allAssessment.objects.filter(assId=ass_id)
    # Retrieves the first 5 question objects for the given ass_id
    allque = allAssessment.objects.get(assId=ass_id).question_set.all()[:5]
    return render(request, 'assview.html', {'ques': allque, 'ass': assessment})

 ##########   Add Question View   ##########
@staff_member_required
@login_required(login_url='login')
def Add_question(request):
    if request.method == 'GET':
        que = request.GET.get('que')
        correctanswer = request.GET.get('correctanswer')
        identi_assessment = request.GET.get('ass')
        ass = allAssessment.objects.get(identi_assessment=identi_assessment)
        ass_id = ass.assId
        new_que = Question()
        new_que.quostion = que
        new_que.correctanswer = correctanswer
        new_que.assessment = ass
        new_que.save()
        return HttpResponseRedirect(reverse("view", args=(ass_id,)))
    return HttpResponseRedirect(reverse("view", args=(ass_id,)))


 ##########   Teste result  template View   ##########
def testresult(request):
    return render(request, 'testresult.html')


 ##########   Teste result  View   ##########
def testresultfunc(request):
    if request.method == 'GET':
        s1 = request.GET.get('s1')
        s2 = request.GET.get('s2')
        accuracy1 = FindAcc(s1, s2)
        accuracy2 = FindAcc2(s1, s2)
        accuracy3 = similarity(s1, s2)
        print(s1)
        print(s2)
        print(accuracy1)
        print(accuracy2)
        print(accuracy3)
    context = {'accuracy1': accuracy1, 'accuracy2': accuracy2, 'accuracy3': round(accuracy3, 2), 's1': s1, 's2': s2}
    return render(request, 'testresult.html', context)

 ##########   Assessments Result generation View   ##########


 ##########   Submistion details view  ##########
def detail_view(request, user_name, assessment_name, identi):
    url = settings.MEDIA_URL
    # Retrieves submission_status objects for the given user name, assessment name, and identi
    sub_status = submission_status.objects.filter(user_name=user_name, assessment_name=assessment_name, identi=identi)
    # Retrieves videoAns objects for the given user name, assessment name, and identi
    data = videoAns.objects.filter(user_name=user_name, assessment_name=assessment_name, identi=identi)
    return render(request, 'use.html', {'data': data, 'sub_status': sub_status, 'url': url, 'user_name': user_name,'assessment_name': assessment_name,'identi': identi})



 ##########   Result View   ##########
@staff_member_required
@login_required(login_url='login')
def run_task(request):
    ref_url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':

        acc = []
        user_name = request.POST.get('user_name')
        assessment_name = request.POST.get('assessment_name')
        identi = request.POST.get('identi')
        video_ans_ids = request.POST.get('video_ans_ids').split(',')
        data = videoAns.objects.filter(user_name=user_name, assessment_name=assessment_name, identi=identi)
        data1 = videoAns.objects.filter(user_name=user_name, assessment_name=assessment_name, identi=identi)
        sub_status = submission_status.objects.get(user_name=user_name, assessment_name=assessment_name, identi=identi)
        sub_status.result_process=True
        sub_status.save()

        for video_ans_id in data1:
            vf = video_ans_id.videoAns.path
            #confidence, nervousness = analyze_video_emotions(vf)
            confidence, nervousness, neutral = analyze_video_emotions(vf)
            print("confidence:", confidence, "%\nnervousness:", nervousness, "%")
            video_ans_id.confidence = confidence
            video_ans_id.nervousness = nervousness
            video_ans_id.neutral = neutral
            video_ans_id.save()

        for video_ans_id in video_ans_ids:
            print(video_ans_id)
            result = videoAns.objects.get(ansId=video_ans_id)
            vf = result.videoAns.path
            import requests
            API_KEY = "623cfea0aba24d8f981195bbc20d48e0"
            filename = vf
            # Upload Module Begins
            def read_file(filename, chunk_size=5242880):
                with open(filename, 'rb') as _file:
                    while True:
                        data = _file.read(chunk_size)
                        if not data:
                            break
                        yield data
            headers = {'authorization': API_KEY}
            response = requests.post('https://api.assemblyai.com/v2/upload', headers=headers, data=read_file(filename))
            json_str1 = response.json()
            
            endpoint = "https://api.assemblyai.com/v2/transcript"
            json = {
                "audio_url": json_str1["upload_url"]
            }
            response = requests.post(endpoint, json=json, headers=headers)
            json_str2 = response.json()
            endpoint = "https://api.assemblyai.com/v2/transcript/" + json_str2["id"]
            response = requests.get(endpoint, headers=headers)
            json_str3 = response.json()
            while json_str3["status"] != "completed":
                response = requests.get(endpoint, headers=headers)
                json_str3 = response.json()
            result.trasnscript = json_str3["text"]
            result.save()
            answer = videoAns.objects.filter(ansId=video_ans_id)
            for trans in answer:
                s1 = trans.question_id.correctanswer
                s2 = trans.trasnscript
            accuracy = FindAcc(s1, s2)
            answer = videoAns.objects.get(ansId=video_ans_id)
            answer.answer_accurecy = accuracy
            answer.save()
            print(s1)
            print(s2)
            answer = videoAns.objects.get(ansId=video_ans_id)
            acc.append(answer.answer_accurecy)
        print(acc)
        mean_acc = mean(acc)
        print("mean of acc is", mean_acc)
        sub_status.final_result = mean_acc
        sub_status.result_generate = True
        sub_status.save()
        messages.success(request, 'Result is generated Successfully.')
    return HttpResponseRedirect(ref_url)
