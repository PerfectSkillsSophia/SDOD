# app_name/tasks.py
from celery import shared_task
import requests
from assessments.models import videoAns
from celery import shared_task
import requests
from assessments.models import videoAns

@shared_task
def upload_and_generate_transcript(video_ans_id):
    try:
        API_KEY = "623cfea0aba24d8f981195bbc20d48e0"
        result = videoAns.objects.get(ansId=video_ans_id)
        vf = result.videoAns.path
        
        def read_file(filename, chunk_size=5242880):
            with open(filename, 'rb') as _file:
                while True:
                    data = _file.read(chunk_size)
                    if not data:
                        break
                    yield data
                    
        headers = {'authorization': API_KEY}
        response = requests.post('https://api.assemblyai.com/v2/upload', headers=headers, data=read_file(vf))
        response.raise_for_status()
        json_str1 = response.json()
        
        endpoint = "https://api.assemblyai.com/v2/transcript"
        json_data = {
            "audio_url": json_str1["upload_url"]
        }
        
        response = requests.post(endpoint, json=json_data, headers=headers)
        response.raise_for_status()
        json_str2 = response.json()
        transcript_id = json_str2["id"]
        
        endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
        while True:
            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()
            json_str3 = response.json()
            if json_str3["status"] == "completed":
                break
        if json_str3["text"]:
            result.trasnscript = json_str3["text"]
            result.save()
        else:
            result.trasnscript = "Answer has not been generated."
            result.save()
    except Exception as e:
        error_message = str(e)
        result.trasnscript = f"Error: {error_message}"
        result.save()

@shared_task
def videoids(ids):
    for i in ids:
        try:
            upload_and_generate_transcript(i)
        except Exception as e:
            continue  # Skip to the next iteration without processing the current i
