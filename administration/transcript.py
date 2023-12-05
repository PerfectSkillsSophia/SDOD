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

