import asyncio
import aiohttp

async def read_file(filename, chunk_size=10485760):
    with open(filename, 'rb') as file:
        while True:
            data = file.read(chunk_size)
            if not data:
                break
            yield data

async def upload_file(API_KEY, filename):
    headers = {'authorization': API_KEY}
    endpoint = 'https://api.assemblyai.com/v2/upload'
    async with aiohttp.ClientSession() as session:
        async for data in read_file(filename):
            async with session.post(endpoint, headers=headers, data=data) as response:
                json_str1 = await response.json()
                await asyncio.sleep(0.1)  # Delay to avoid rate limits
                audio_url = json_str1['upload_url']
                return audio_url

async def get_transcript(API_KEY, audio_url):
    headers = {'authorization': API_KEY}
    endpoint = 'https://api.assemblyai.com/v2/transcript'
    json_data = {'audio_url': audio_url}
    async with aiohttp.ClientSession() as session:
        async with session.post(endpoint, json=json_data, headers=headers) as response:
            json_str2 = await response.json()
            transcript_id = json_str2['id']
            while True:
                async with session.get(endpoint + '/' + transcript_id, headers=headers) as response:
                    json_str3 = await response.json()
                    if json_str3['status'] == 'completed':
                        return json_str3['text']
                    await asyncio.sleep(1)  # Delay to avoid rate limits

async def transcribe_audio(API_KEY, filename):
    audio_url = await upload_file(API_KEY, filename)
    transcription = await get_transcript(API_KEY, audio_url)
    return transcription