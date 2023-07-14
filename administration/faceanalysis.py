###############    FER    ###################
from fer import FER
import cv2
from django.conf import settings
import os
from django.core.files.storage import default_storage
def analyze_video_emotions(video_path):
    vid = cv2.VideoCapture(video_path)
    if not vid.isOpened():
        raise ValueError("Could not open the video file")

    fps = vid.get(cv2.CAP_PROP_FPS)
    fps = int(fps)
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
                sad1 += attri[0]["emotions"].get('sad', 0)
                fear1 += attri[0]["emotions"].get('fear', 0)
                happy1 += attri[0]["emotions"].get('happy', 0)
                angry1 += attri[0]["emotions"].get('angry', 0)
                surprise1 += attri[0]["emotions"].get('surprise', 0)
                disgust1 += attri[0]["emotions"].get('disgust', 0)
                neutral1 += attri[0]["emotions"].get('neutral', 0)
                i += 1
            else:
                break
        n += 1

    vid.release()
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    for i in range(1, 5):
        cv2.waitKey(1)

    total = sad1 + fear1 + happy1 + angry1 + surprise1 + disgust1 + neutral1
    confidence = ((happy1 + angry1 + surprise1 + disgust1) / total) * 100 if total > 0 else 0
    nervousness = ((sad1 + fear1) / total) * 100 if total > 0 else 0
    neutral1 = (neutral1 / total) * 100 if total > 0 else 0

    if confidence > nervousness:
        confidence += neutral1
    else:
        nervousness += neutral1

    return confidence, nervousness


# Example usage:
# Example usage:






