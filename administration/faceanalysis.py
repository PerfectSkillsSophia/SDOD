###############    FER    ###################
from fer import FER
import cv2
from django.conf import settings
import os
from django.core.files.storage import default_storage
""" def analyze_video_emotions(video_path):
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
 """

import cv2
from fer import FER
import math

def analyze_video_emotions(video_filename):
    vid = cv2.VideoCapture(video_filename)
    fps = int(vid.get(cv2.CAP_PROP_FPS) / 3)  # Process every third frame
    emotion_detector = FER()
    n = 0
    i = 0
    sad1 = fear1 = happy1 = angry1 = surprise1 = disgust1 = neutral1 = 0

    while True:
        ret, frame = vid.read()
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
            else:
                break
        n += 1
        if ret == False:
            break
    vid.release()
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    for i in range(1, 5):
        cv2.waitKey(1)

    total = sad1 + fear1 + happy1 + angry1 + surprise1 + disgust1 + neutral1
    total2 = happy1 + surprise1 + sad1 + fear1 + disgust1
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

# # Example usage:
# video_filename = "JustEx.mp4"
# confidence, nervousness, neutral = analyze_video_emotion(video_filename)
# print("Confidence:", confidence, "%")
# print("Nervousness:", nervousness, "%")
# print("Neutral:", neutral, "%")
