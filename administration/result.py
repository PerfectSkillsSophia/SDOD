import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.data.path.append('nltk_data')

# import nltk
# import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download('wordnet')

def FindAcc(S1, S2):
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


# X = "i am not batman" # fixed i.e teacher
# Y = "i am batman" #trascript

# print("similarity:", similarity(X, Y))
