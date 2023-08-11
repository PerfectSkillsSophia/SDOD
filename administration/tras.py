import moviepy.editor as mp
import speech_recognition as sr

def generate_transcript(video_path):
    # Load the video
    video = mp.VideoFileClip(video_path)
    
    # Extract audio from the video
    audio = video.audio
    
    # Save the extracted audio to a temporary WAV file
    temp_audio_path = "temp_audio.wav"
    audio.write_audiofile(temp_audio_path)
    
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    
    # Load the audio file
    with sr.AudioFile(temp_audio_path) as source:
        # Adjust for ambient noise levels
        recognizer.adjust_for_ambient_noise(source)
        
        # Recognize the speech
        audio_text = recognizer.recognize_google(source)
    
    # Close the temporary audio file
    audio.close()
    
    # Return the generated transcript
    return audio_text
