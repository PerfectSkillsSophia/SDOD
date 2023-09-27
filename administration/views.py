##########   NEW CODE   ##########

from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from assessments.models import *
from django.contrib import messages
from administration.models import *
from django.urls import reverse
from sophia import settings
import random
import string
from .func import *
from .transcript import upload_and_transcribe_audio
from statistics import mean


 ##########   Dashboard View   ##########
@staff_member_required
@login_required(login_url='login')
def dashboard(request):
    # Retrieves all assessment objects
    assessment = allAssessment.objects
    return render(request, 'dashboard.html', {'assessment': assessment})

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
    allque = allAssessment.objects.get(assId=ass_id).question_set.all()[:10]
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


 ##########   Submistion details view  ##########
def detail_view(request, identi):
    url = settings.MEDIA_URL
    sub_status = submission_status.objects.filter(identi=identi)
    return render(request, 'use.html', { 'sub_status': sub_status, 'url': url})



 ##########   Result View   ##########
@staff_member_required
@login_required(login_url='login')
def run_task(request):
    ref_url = request.META.get('HTTP_REFERER')
    acc = []
    if request.method == 'POST':
        identi = request.POST.get('identi')
        sub_status_instance = submission_status.objects.get(identi=identi)
        video_ans_instances = sub_status_instance.video_answers.all()  # Get all associated videoAns instances
        ans_id_video_dict = {video_ans.ansId: video_ans.videoAns.path for video_ans in video_ans_instances}
        sub_status_instance.result_process=True
        sub_status_instance.save()
        for id, video_file in ans_id_video_dict.items():
            result = sub_status_instance.video_answers.get(ansId = id)
            vf = video_file
            confidence, nervousness, neutral = analyze_video_emotions(vf)
            result.confidence=confidence
            result.nervousness=nervousness
            result.neutral=neutral
            result.save()
        for id, video_file in ans_id_video_dict.items():
            result = sub_status_instance.video_answers.get(ansId = id)
            vf = video_file
            transcript = upload_and_transcribe_audio(vf)
            result.trasnscript = transcript
            result.save()
            s1 = result.question_id.correctanswer
            s2 = result.trasnscript
            print("s1" ,s1,"s2",s2)
            text_percetage = FindAcc(s1, s2)
            result.answer_accurecy = text_percetage
            result.save()
            acc.append(text_percetage)

        sub_status_instance.final_result = mean(acc)
        sub_status_instance.result_generate = True
        sub_status_instance.save()
        messages.success(request, 'Result is generated Successfully.')
    return HttpResponseRedirect(ref_url)



            