from deepface import DeepFace
import cv2
import os
from sophia import settings

def analyze_emotions(vf):
    try:
        # Open video file
        vid = cv2.VideoCapture(vf)

        # Get the frames per second (fps) of the video
        fps = vid.get(cv2.CAP_PROP_FPS)
        fps = int(fps)

        n = 0
        i = 0
        emotions = {
            'sad': 0,
            'fear': 0,
            'happy': 0,
            'angry': 0,
            'surprise': 0,
            'disgust': 0,
            'neutral': 0
        }

        while True:
            ret, frame = vid.read()

            # Save every nth frame as an image and analyze it
            if n % fps == 0:
                image_path = os.path.join(settings.MEDIA_ROOT, f"frame_{i}.jpg")
                cv2.imwrite(image_path, frame)
                attr = DeepFace.analyze(img_path=image_path, actions=['emotion'], enforce_detection=False)
                emotion = attr[0]["emotion"]
                for emotion_label, emotion_value in emotion.items():
                    emotions[emotion_label] += emotion_value
                i += 1

            n += 1
            if ret is False:
                break

        vid.release()
        cv2.destroyAllWindows()

        # Calculate the total emotions
        total = sum(emotions.values())

        # Calculate confidence and nervousness percentages
        confidence = ((emotions['happy'] + emotions['angry'] + emotions['surprise'] + emotions['disgust']) / total) * 100
        nervousness = ((emotions['sad'] + emotions['fear']) / total) * 100

        # Adjust confidence and nervousness based on neutral emotion
        if confidence > nervousness:
            confidence += emotions['neutral']
        else:
            nervousness += emotions['neutral']

        return confidence, nervousness

    except Exception as e:
        # Handle any errors that may occur
        print("Error:", str(e))
        return None, None
