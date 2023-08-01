""" from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from assessments.models import *
from django.contrib import messages
from assessments.models import *
from administration.models import *
from django.urls import reverse
from django.db.models import Q
from sophia import settings
from .result import *
from statistics import mean
import random
import string
from faceanalysis import analyze_video_emotions

@staff_member_required
@login_required(login_url='login')
def dashboard(request):
    assessment = allAssessment.objects
    video = videoAns.objects.all()[:5]
    return render(request, 'dashboard.html', {'assessment': assessment, 'video': video})


@staff_member_required
@login_required(login_url='login')
def allAnswer(request):
    all_data = videoAns.objects.all().values(
        'user_name', 'assessment_name', 'identi').distinct()

    # return render(request, 'all_submmision.html', {'video': video, 'url': url})
    return render(request, 'submmision.html', {'all_data': all_data})


@staff_member_required
@login_required(login_url='login')
def detail_view(request, user_name, assessment_name, identi):
    url = settings. MEDIA_URL
    sub_status = submission_status.objects.filter(
        user_name=user_name, assessment_name=assessment_name, identi=identi)
    data = videoAns.objects.filter(
        user_name=user_name, assessment_name=assessment_name, identi=identi)
    return render(request, 'detail.html', {'data': data,'sub_status': sub_status,'url': url, 'user_name': user_name,})

@staff_member_required
@login_required(login_url='login')
def searchbar(request):
    query = request.GET.get('q')
    url = settings. MEDIA_URL
    if query:
        results = videoAns.objects.filter(
            Q(user_name__icontains=query) | Q(assessment_name__icontains=query))
    else:
        results = videoAns.objects.all()
    return render(request, 'all_submmision.html', {'results': results, 'query': query, 'url': url})


@staff_member_required
@login_required(login_url='login')
def add_assessment(request):
    return render(request, 'add_assessments.html')


@staff_member_required
@login_required(login_url='login')
def Add_assessment(request):
    if request.method == 'GET':
        ass_name = request.GET.get('ass_name')
        ass_dec = request.GET.get('ass_dec')
        random_number = random.choice(string.digits)
        random_character = random.choice(string.ascii_letters)
        identi_assessment =ass_name + "_" + random_number + random_character
        new_ass = allAssessment()
        new_ass.assessmentName = ass_name
        new_ass.assessmentDes = ass_dec
        new_ass.identi_assessment = identi_assessment
        new_ass.save()
        return redirect('addassessment')
    return redirect('addassessment')


@staff_member_required
@login_required(login_url='login')
def view_assessments(request, ass_id):
    ass_id = ass_id
    assessment = allAssessment.objects.filter(assId=ass_id)
    allque = allAssessment.objects.get(assId=ass_id).question_set.all()[:5]
    return render(request, 'assview.html', {'ques': allque, 'ass': assessment})


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
    context = {'accuracy1': accuracy1, 'accuracy2': accuracy2,
               'accuracy3': round(accuracy3, 2), 's1': s1, 's2': s2}
    return render(request, 'testresult.html', context)


def testresult(request):

    return render(request, 'testresult.html')


@staff_member_required
@login_required(login_url='login')
def run_task(request):
    ref_url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        acc=[]
        user_name = request.POST.get('user_name')
        assessment_name = request.POST.get('assessment_name')
        identi = request.POST.get('identi')
        video_ans_ids = request.POST.get('video_ans_ids').split(',')
        data = videoAns.objects.filter(
        user_name=user_name, assessment_name=assessment_name, identi=identi)
        data1 = videoAns.objects.filter(
        user_name=user_name, assessment_name=assessment_name, identi=identi)
        for video_ans_id in data1:
            #media_folder_path = settings.MEDIA_ROOT
            vf=video_ans_id.videoAns.path
            #video_path = os.path.join(media_folder_path, str(vf))
            confidence, nervousness = analyze_video_emotions(vf)
            print("confidence:", confidence, "%\nnervousness:", nervousness, "%")
            # confidence, nervousness = analyze_emotions(vf)
            # if confidence is not None and nervousness is not None:
            #     print("Confidence:", confidence, "%")
            #     print("Nervousness:", nervousness, "%")
            video_ans_id.confidence=confidence
            video_ans_id.nervousness=nervousness
            video_ans_id.save()

            # else:
            #     print("Error occurred during analysis.")

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
            response = requests.post('https://api.assemblyai.com/v2/upload',
									headers=headers,
									data=read_file(filename))
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
        print("mean of acc is",mean_acc)
        sub_status = submission_status.objects.get(
        user_name=user_name, assessment_name=assessment_name, identi=identi)
        sub_status.final_result=mean_acc
        sub_status.result_generate=True
        sub_status.save()
        messages.success(request, 'Result is generated Successfully.')
    return HttpResponseRedirect(ref_url,{'mean_acc':mean_acc})
 """


 ##########   NEW CODE   ##########

from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from assessments.models import *
from django.contrib import messages
from assessments.models import *
from administration.models import *
from django.urls import reverse
from django.db.models import Q
from sophia import settings
from .result import *
from statistics import mean
import random
import string
from .faceanalysis import analyze_video_emotions


from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from PIL import Image
import io
from reportlab.pdfgen import canvas






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

 ##########   Result View   ##########

def detail_view(request, user_name, assessment_name, identi):
    url = settings.MEDIA_URL
    # Retrieves submission_status objects for the given user name, assessment name, and identi
    sub_status = submission_status.objects.filter(user_name=user_name, assessment_name=assessment_name, identi=identi)
    # Retrieves videoAns objects for the given user name, assessment name, and identi
    data = videoAns.objects.filter(user_name=user_name, assessment_name=assessment_name, identi=identi)
    return render(request, 'detail.html', {'data': data, 'sub_status': sub_status, 'url': url, 'user_name': user_name,'assessment_name': assessment_name,'identi': identi})

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
        sub_status = submission_status.objects.get(user_name=user_name, assessment_name=assessment_name, identi=identi)
        sub_status.final_result = mean_acc
        sub_status.result_generate = True
        sub_status.save()
        messages.success(request, 'Result is generated Successfully.')
    return HttpResponseRedirect(ref_url, {'mean_acc': mean_acc})



 ##########   Result View   ##########




def take_full_page_screenshot(url):
    try:
        # Configure the Chrome options
        chrome_options = Options()
        # Use the headless mode to run without opening a browser window
        chrome_options.add_argument("--headless")
        # Create a new instance of the Chrome driver
        driver = webdriver.Chrome(options=chrome_options)
        # Set up the Selenium WebDriver
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--start-maximized")
        chrome_options = webdriver.Chrome(options=Options)
        # Load the HTML page
        driver.get(url)

        # Wait for the page to load completely (you can adjust the time depending on the page's content)
        time.sleep(5)

        # Get the full height of the web page
        total_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")

        # Set the browser window size to the full height of the web page
        driver.set_window_size(driver.execute_script("return window.innerWidth"), total_height)

        # Take a screenshot of the visible area of the web page
        screenshot = driver.get_screenshot_as_png()

        # Convert the screenshot data to a PIL.Image object
        screenshot_image = Image.open(io.BytesIO(screenshot))

        # Close the driver
        driver.quit()

        return screenshot_image
    except Exception as e:
        print("Error: ", e)
        return None

def generate_pdf_from_screenshot(screenshot):
    # Create a new PDF buffer
    pdf_buffer = io.BytesIO()

    # Draw the screenshot on the PDF
    c = canvas.Canvas(pdf_buffer, pagesize=screenshot.size)
    c.drawInlineImage(screenshot, 0, 0, width=screenshot.width, height=screenshot.height)
    c.save()

    # Return the PDF buffer
    return pdf_buffer.getvalue()

def screenshot_to_pdf(request, slug1, slug2, slug3):
    # Replace 'your_html_page_url' with the actual URL of the HTML page you want to capture
    html_page_url = f'https://psautoscreen.com/administration/detail/{slug1}/{slug2}/{slug3}/'
    full_page_screenshot = take_full_page_screenshot(html_page_url)
    if full_page_screenshot:
        pdf_buffer = generate_pdf_from_screenshot(full_page_screenshot)
        # Set the appropriate response headers for a PDF file
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename= "Result.pdf"'
        return response
    else:
        return HttpResponse("Failed to capture the full-page screenshot.")
