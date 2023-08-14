import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.data.path.append('nltk_data')
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import cv2
from fer import FER
import math
import time
import io
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from reportlab.pdfgen import canvas
from django.http import HttpResponse
###############    FER    ###################


def analyze_video_emotions(video_filename):
    vid = cv2.VideoCapture(video_filename)
    fps = int(vid.get(cv2.CAP_PROP_FPS) / 3)  # Process every third frame
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
                sad1 += attri[0]["emotions"]['sad']
                fear1 += attri[0]["emotions"]['fear']
                happy1 += attri[0]["emotions"]['happy']
                angry1 += attri[0]["emotions"]['angry']
                surprise1 += attri[0]["emotions"]['surprise']
                disgust1 += attri[0]["emotions"]['disgust']
                neutral1 += attri[0]["emotions"]['neutral']
                i += 1
        n += 1
    vid.release()

    total = sad1 + fear1 + happy1 + angry1 + surprise1 + disgust1 + neutral1
    
    if total == 0:
        confidence = 0
        nervousness = 0
    else:
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


##############################

def FindAcc(S1, S2):
    X = S1.lower()
    Y = S2.lower()

    S1 = re.split(r'[ ,.!;"()]', X)
    S2 = re.split(r'[ ,.!;"()]', Y)

    S1.sort()
    S2.sort()

    Positive = 0
    Negative = 0

    if len(S1) == 1:
        if S1[0] in S2:
            AccPer = 100
        else:
            AccPer = 0
        return AccPer

    if len(S2) == 1:
        S2.append(".")

    for i in S1:
        if i == "":
            continue

        if i in S2:
            Positive += 1
        else:
            Negative += 1

    Total = Positive + Negative

    AccPer = (Positive * 100) / Total

    if Negative < 5:
        X_list = word_tokenize(X)
        Y_list = word_tokenize(Y)

        sw = stopwords.words("english")
        l1 = []
        l2 = []

        X_set = {w for w in X_list if not w in sw}
        Y_set = {w for w in Y_list if not w in sw}

        rvector = X_set.union(Y_set)
        for w in rvector:
            if w in X_set:
                l1.append(1)  # create a vector
            else:
                l1.append(0)
            if w in Y_set:
                l2.append(1)
            else:
                l2.append(0)
        c = 0

        for i in range(len(rvector)):
            c += l1[i] * l2[i]
        cosine = c / float((sum(l1) * sum(l2)) ** 0.5)

        if min(AccPer, (cosine * 100)) < 40:
            AccPer = min(AccPer, cosine)
        else:
            AccPer = max(AccPer, cosine)

    return AccPer

#################################
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def FindAcc2(S1, S2):
    X = S1.lower()
    Y = S2.lower()

    S1 = re.split(r'[ ,.!;"()]', X)
    S2 = re.split(r'[ ,.!;"()]', Y)

    S1.sort()
    S2.sort()

    Positive = 0
    Negative = 0

    for i in S1:
        if i == "":
            continue

        if i in S2:
            Positive += 1
        else:
            Negative += 1

    Total = Positive + Negative

    AccPer = (Positive * 100) / Total

    X_list = word_tokenize(X)
    Y_list = word_tokenize(Y)

    sw = stopwords.words("english")
    l1 = []
    l2 = []

    X_set = {w for w in X_list if not w in sw}
    Y_set = {w for w in Y_list if not w in sw}

    rvector = X_set.union(Y_set)
    for w in rvector:
        if w in X_set:
            l1.append(1)  # create a vector
        else:
            l1.append(0)
        if w in Y_set:
            l2.append(1)
        else:
            l2.append(0)
    c = 0

    for i in range(len(rvector)):
        c += l1[i] * l2[i]
    cosine = c / float((sum(l1) * sum(l2)) ** 0.5)

    cosine *= 100

    if min(AccPer, (cosine)) < 40:
        AccPer = min(AccPer, cosine)
    # elif AccPer - cosine > 20:
    # AccPer = cosine
    else:
        AccPer = max(AccPer, cosine)

    if (not ("not" in S1 and "not" in S2)) and ("not" in S1 or "not" in S2):
        AccPer = 100 - AccPer

    return AccPer



###########


# Calculates semantic similarity using Wordnet's Gene Ontology
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
import re
import nltk
nltk.data.path.append('nltk_data')

def similarity(X, Y):
    S1 = re.split(r'[ ,.!;"()]', X)
    S2 = re.split(r'[ ,.!;"()]', Y)

    def penn_to_wn(tag):
        """Convert between a Penn Treebank tag to a simplified Wordnet tag"""
        if tag.startswith("N"):
            return "n"

        if tag.startswith("V"):
            return "v"

        if tag.startswith("J"):
            return "a"

        if tag.startswith("R"):
            return "r"

        return None

    def tagged_to_synset(word, tag):
        wn_tag = penn_to_wn(tag)
        if wn_tag is None:
            return None

        try:
            return wn.synsets(word, wn_tag)[0]
        except:
            return None

    def sentence_similarity(sentence1, sentence2):
        """compute the sentence similarity using Wordnet"""
        # Tokenize and tag
        sentence1 = pos_tag(word_tokenize(sentence1))
        sentence2 = pos_tag(word_tokenize(sentence2))

        # Get the synsets for the tagged words
        synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in sentence1]
        synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in sentence2]

        # Filter out the Nones
        synsets1 = [ss for ss in synsets1 if ss]
        synsets2 = [ss for ss in synsets2 if ss]

        score, count = 0.0,0

        # For each word in the first sentence
        for synset in synsets1:
            # Get the similarity value of the most similar word in the other sentence
            best_score = max([synset.path_similarity(ss) for ss in synsets2])

            # Check that the similarity could have been computed
            if best_score is not None:
                score += best_score
                count += 1

        # Average the values
        print(score)
        print(count)
        score /= count
        return score

    sentences = [
        Y,
    ]

    focus_sentence = X

    for sentence in sentences:
        accu = sentence_similarity(focus_sentence, sentence)
        accu *= 100

    if (not ("not" in S1 and "not" in S2)) and ("not" in S1 or "not" in S2):
        accu = 100 - accu

    return accu
 

###############################

def take_full_page_screenshot(url, max_retries=3):
    for _ in range(max_retries):
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-gpu")
            driver = webdriver.Chrome(options=chrome_options)

            driver.get(url)
            time.sleep(10)  # Wait for the page to load (adjust as needed)

            total_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
            driver.set_window_size(driver.execute_script("return window.innerWidth"), total_height)

            screenshot = driver.get_screenshot_as_png()
            screenshot_image = Image.open(io.BytesIO(screenshot))

            driver.quit()

            return screenshot_image
        except Exception as e:
            print(f"Error: {e}\nRetrying...")
            time.sleep(5)  # Wait before retrying

    return f"Failed to capture the full-page screenshot for URL: {url}"

def generate_pdf_from_screenshot(screenshot):
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=screenshot.size)
    c.drawInlineImage(screenshot, 0, 0, width=screenshot.width, height=screenshot.height)
    c.save()
    return pdf_buffer.getvalue()


