# from deepface import DeepFace
# import cv2
# import os
# from sophia import settings

# def analyze_emotions(vf):
#     try:
#         # Open video file
#         vid = cv2.VideoCapture(vf)

#         # Get the frames per second (fps) of the video
#         fps = vid.get(cv2.CAP_PROP_FPS)
#         fps = int(fps)

#         n = 0
#         i = 0
#         emotions = {
#             'sad': 0,
#             'fear': 0,
#             'happy': 0,
#             'angry': 0,
#             'surprise': 0,
#             'disgust': 0,
#             'neutral': 0
#         }

#         while True:
#             ret, frame = vid.read()

#             # Save every nth frame as an image and analyze it
#             if n % fps == 0:
#                 image_path = os.path.join(settings.MEDIA_ROOT, f"frame_{i}.jpg")
#                 cv2.imwrite(image_path, frame)
#                 attr = DeepFace.analyze(img_path=image_path, actions=['emotion'], enforce_detection=False)
#                 emotion = attr[0]["emotion"]
#                 for emotion_label, emotion_value in emotion.items():
#                     emotions[emotion_label] += emotion_value
#                 i += 1

#             n += 1
#             if ret is False:
#                 break

#         vid.release()
#         cv2.destroyAllWindows()

#         # Calculate the total emotions
#         total = sum(emotions.values())

#         # Calculate confidence and nervousness percentages
#         confidence = ((emotions['happy'] + emotions['angry'] + emotions['surprise'] + emotions['disgust']) / total) * 100
#         nervousness = ((emotions['sad'] + emotions['fear']) / total) * 100

#         # Adjust confidence and nervousness based on neutral emotion
#         if confidence > nervousness:
#             confidence += emotions['neutral']
#         else:
#             nervousness += emotions['neutral']

#         return confidence, nervousness

#     except Exception as e:
#         # Handle any errors that may occur
#         print("Error:", str(e))
#         return None, None






###############    FER    ###################

from fer import FER
import cv2

# def analyze_video_emotions(video_path):
#     vid = cv2.VideoCapture(video_path)
#     fps = vid.get(cv2.CAP_PROP_FPS)
#     fps = int(fps)
#     emotion_detector = FER()
#     n = 0
#     i = 0
#     sad1 = fear1 = happy1 = angry1 = surprise1 = disgust1 = neutral1 = 0

#     while True:
#         ret, frame = vid.read()
#         if n % fps == 0:
#             attri = emotion_detector.detect_emotions(frame)
#             print(attri)
#             if len(attri) > 0:
#                 sad1 += attri[0]["emotions"]['sad']
#                 fear1 += attri[0]["emotions"]['fear']
#                 happy1 += attri[0]["emotions"]['happy']
#                 angry1 += attri[0]["emotions"]['angry']
#                 surprise1 += attri[0]["emotions"]['surprise']
#                 disgust1 += attri[0]["emotions"]['disgust']
#                 neutral1 += attri[0]["emotions"]['neutral']
#                 i += 1
#             else:
#                 break
#         n += 1
#         if ret == False:
#             break

#     vid.release()
#     cv2.waitKey(1)
#     cv2.destroyAllWindows()
#     for i in range(1, 5):
#         cv2.waitKey(1)

#     total = sad1 + fear1 + happy1 + angry1 + surprise1 + disgust1 + neutral1
#     confidence = ((happy1 + angry1 + surprise1 + disgust1) / total) * 100
#     nervousness = ((sad1 + fear1) / total) * 100
#     neutral1 = (neutral1 / total) * 100

#     if confidence > nervousness:
#         confidence += neutral1
#     else:
#         nervousness += neutral1

#     return confidence, nervousness

# Example usage:

