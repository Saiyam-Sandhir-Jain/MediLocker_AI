import json
import pandas as pd
import spacy
import joblib
import numpy as np
import itertools
import csv
import re
from django.http import JsonResponse
from django.shortcuts import render
from spacy.lang.en.stop_words import STOP_WORDS
from nltk.wsd import lesk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from django.views.decorators.csrf import csrf_exempt

import os

# Get the absolute path to the base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Paths to your dataset files
TRAINING_CSV_PATH = os.path.join(BASE_DIR, 'chatbot', 'static', 'Medical_dataset', 'Training.csv')
TESTING_CSV_PATH = os.path.join(BASE_DIR, 'chatbot', 'static', 'Medical_dataset', 'Testing.csv')
DATA_JSON_PATH = os.path.join(BASE_DIR, 'chatbot', 'static', 'DATA.json')
MODEL_PATH = os.path.join(BASE_DIR, 'chatbot', 'static','model', 'knn.pkl')
SYMPTOM_DESCRIPTION_CSV = os.path.join(BASE_DIR, 'chatbot', 'static', 'Medical_dataset', 'symptom_Description.csv')
SYMPTOM_SEVERITY_CSV = os.path.join(BASE_DIR, 'chatbot', 'static', 'Medical_dataset', 'symptom_severity.csv')
SYMPTOM_PRECAUTION_CSV = os.path.join(BASE_DIR, 'chatbot', 'static', 'Medical_dataset', 'symptom_precaution.csv')

# Use absolute paths
df_tr = pd.read_csv(os.path.join(BASE_DIR, TRAINING_CSV_PATH))
df_tt = pd.read_csv(os.path.join(BASE_DIR, TESTING_CSV_PATH))


# Initialize data
data = {"users": []}
with open('DATA.json', 'w') as outfile:
    json.dump(data, outfile)

def write_json(new_data, filename=DATA_JSON_PATH):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        file_data["users"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)

# Initialize symptoms and diseases
symp = []
disease = []
for i in range(len(df_tr)):
    symp.append(df_tr.columns[df_tr.iloc[i] == 1].to_list())
    disease.append(df_tr.iloc[i, -1])

# Get all symptoms
all_symp_col = list(df_tr.columns[:-1])

def clean_symp(sym):
    return sym.replace('_', ' ').replace('.1', '').replace('(typhos)', '').replace('yellowish', 'yellow').replace('yellowing', 'yellow')

all_symp = [clean_symp(sym) for sym in all_symp_col]

# Preprocess symptoms
nlp = spacy.load("en_core_web_sm")  # Load the spacy model
def preprocess(doc):
    nlp_doc = nlp(doc)
    d = []
    for token in nlp_doc:
        if (not token.text.lower() in STOP_WORDS and token.text.isalpha()):
            d.append(token.lemma_.lower())
    return ' '.join(d)

all_symp_pr = [preprocess(sym) for sym in all_symp]
col_dict = dict(zip(all_symp_pr, all_symp_col))

# Syntactic Similarity Functions
def powerset(seq):
    if len(seq) <= 1:
        yield seq
        yield []
    else:
        for item in powerset(seq[1:]):
            yield [seq[0]] + item
            yield item

def sort(a):
    a.sort(key=len)
    a.pop()
    return a

def permutations(s):
    return [' '.join(p) for p in itertools.permutations(s)]

def DoesExist(txt):
    txt = txt.split(' ')
    combinations = [x for x in powerset(txt)]
    sort(combinations)
    for comb in combinations:
        for sym in permutations(comb):
            if sym in all_symp_pr:
                return sym
    return False

def jaccard_set(str1, str2):
    list1 = str1.split(' ')
    list2 = str2.split(' ')
    intersection = len(set(list1).intersection(list2))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union

def syntactic_similarity(symp_t, corpus):
    most_sim = []
    poss_sym = []
    for symp in corpus:
        d = jaccard_set(symp_t, symp)
        most_sim.append(d)
    order = np.argsort(most_sim)[::-1].tolist()
    for i in order:
        if DoesExist(symp_t):
            return 1, [corpus[i]]
        if corpus[i] not in poss_sym and most_sim[i] != 0:
            poss_sym.append(corpus[i])
    return (1, poss_sym) if poss_sym else (0, None)

def check_pattern(inp, dis_list):
    pred_list = []
    regexp = re.compile(inp)
    for item in dis_list:
        if regexp.search(item):
            pred_list.append(item)
    return (1, pred_list) if pred_list else (0, None)

# Semantic Similarity Functions
def WSD(word, context):
    return lesk(context, word)

def semanticD(doc1, doc2):
        doc1_p = preprocess(doc1).split(' ')
        doc2_p = preprocess(doc2).split(' ')
        score = 0
        for tock1 in doc1_p:
            for tock2 in doc2_p:
                syn1 = WSD(tock1, doc1)
                syn2 = WSD(tock2, doc2)
                if syn1 is not None and syn2 is not None:
                    x = syn1.wup_similarity(syn2)
                    if x is not None and x > 0.25:
                        score += x
        return score / (len(doc1_p) * len(doc2_p)) if len(doc1_p) * len(doc2_p) > 0 else 0

def semantic_similarity(symp_t, corpus):
    max_sim = 0
    most_sim = None
    for symp in corpus:
        d = semanticD(symp_t, symp)
        if d > max_sim:
            most_sim = symp
            max_sim = d
    return max_sim, most_sim

def suggest_syn(sym):
    symp = []
    synonyms = wordnet.synsets(sym)
    lemmas = [word.lemma_names() for word in synonyms]
    lemmas = list(set(itertools.chain(*lemmas)))
    for e in lemmas:
        res, sym1 = semantic_similarity(e, all_symp_pr)
        if res != 0:
            symp.append(sym1)
    return list(set(symp))

# One-Hot-Vector dataframe
def OHV(cl_sym, all_sym):
    l = np.zeros([1, len(all_sym)])
    for sym in cl_sym:
        l[0, all_sym.index(sym)] = 1
    return pd.DataFrame(l, columns=all_sym)

def contains(small, big):
    return all(i in big for i in small)

# List of symptoms -> possible diseases
def possible_diseases(l):
    poss_dis = []
    for dis in set(disease):
        if contains(l, symVONdisease(df_tr, dis)):
            poss_dis.append(dis)
    return poss_dis

# Disease -> all symptoms
def symVONdisease(df, disease):
    ddf = df[df.prognosis == disease]
    m2 = (ddf == 1).any()
    return m2.index[m2].tolist()

# Load the KNN model
knn_clf = joblib.load(MODEL_PATH)

# Load dictionaries for severity, description, and precautions
severityDictionary = {}
description_list = {}
precautionDictionary = {}

def getDescription():
    global description_list
    with open(SYMPTOM_DESCRIPTION_CSV) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            description_list[row[0]] = row[1]

def getSeverityDict():
    global severityDictionary
    severityDictionary = {}  

    print(f"Loading severity data from: {SYMPTOM_SEVERITY_CSV}")  

    try:
        with open(SYMPTOM_SEVERITY_CSV, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            
            header = next(csv_reader, None)
            if header:
                print(f"Header: {header}")  
            for row_number, row in enumerate(csv_reader, start=1):  
                if not row: 
                    print(f"Skipping empty row at line {row_number}")
                    continue

                if len(row) >= 2:
                    try:
                        symptom = row[0].strip()
                        severity = int(row[1].strip())
                        severityDictionary[symptom] = severity
                    except ValueError as e:
                        print(f"Skipping row {row_number} due to invalid severity value: {row[1]}. Error: {e}")
                else:
                    print(f"Skipping malformed row at line {row_number}: {row}")

    except FileNotFoundError:
        print(f"Error: The file '{SYMPTOM_SEVERITY_CSV}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred while reading the CSV file: {e}")

    print(f"Loaded severity dictionary: {severityDictionary}")

def getprecautionDict():
    global precautionDictionary
    with open(SYMPTOM_PRECAUTION_CSV) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            precautionDictionary[row[0]] = [row[1], row[2], row[3], row[4]]

# Load dictionaries
getSeverityDict()
getprecautionDict()
getDescription()

# Calculate patient condition
def calc_condition(exp, days):
    total_severity = sum(severityDictionary.get(item, 0) for item in exp)
    if (total_severity * days) / len(exp) > 13:
        return 1  # Should consult a doctor
    else:
        return 0  # Might not be serious

# Print possible symptoms
def related_sym(psym1):
    s = "Could you be more specific? <br>"
    for num, it in enumerate(psym1):
        s += f"{num}) {clean_symp(it)}<br>"
    return s if psym1 else 0

# Django Views
def chat(request):
    return render(request, 'chatbot.html')

@csrf_exempt
def get_bot_response(request):
    if request.method == 'GET':
        msg = request.GET.get('msg', '')
        s = msg.strip()  # Clean the input message

        if "step" in request.session:
            if request.session["step"] == "Q_C":
                name = request.session["name"]
                age = request.session["age"]
                gender = request.session["gender"]
                request.session.clear()
                if s == "q":
                    return JsonResponse({"response": "Thank you for using our website, Mr/Ms " + name})

            if s.upper() == "OK":
                return JsonResponse({"response": "What is your name?"})

            if 'name' not in request.session and 'step' not in request.session:
                request.session['name'] = s
                request.session['step'] = "age"
                return JsonResponse({"response": "How old are you?"})

            if request.session["step"] == "age":
                request.session["age"] = int(s)
                request.session["step"] = "gender"
                return JsonResponse({"response": "Can you specify your gender?"})

            if request.session["step"] == "gender":
                request.session["gender"] = s
                request.session["step"] = "Depart"

            if request.session['step'] == "Depart":
                request.session['step'] = "BFS"
                return JsonResponse({"response": f"Well, Hello again Mr/Ms {request.session['name']}, now I will be asking a few questions about your symptoms to see what you should do. Tap S to start diagnostic!"})

            if request.session['step'] == "BFS":
                request.session['step'] = "FS"  # first symptom
                return JsonResponse({"response": f"Can you specify your main symptom, Mr/Ms {request.session['name']}?"})

            if request.session['step'] == "FS":
                sym1 = preprocess(s)
                sim1, psym1 = syntactic_similarity(sym1, all_symp_pr)
                request.session['FSY'] = [sym1, sim1, psym1]
                request.session['step'] = "SS"  # second symptom
                if sim1 == 1:
                    request.session['step'] = "RS1"  # related_sym1
                    response = related_sym(psym1)
                    if response != 0:
                        return JsonResponse({"response": response})
                else:
                    return JsonResponse({"response": "You are probably facing another symptom. If so, can you specify it?"})

            if request.session['step'] == "RS1":
                temp = request.session['FSY']
                psym1 = temp[2]
                psym1 = psym1[int(s)]
                temp[2] = psym1
                request.session['FSY'] = temp
                request.session['step'] = 'SS'
                return JsonResponse({"response": "You are probably facing another symptom. If so, can you specify it?"})

            if request.session['step'] == "SS":
                sym2 = preprocess(s)
                sim2, psym2 = syntactic_similarity(sym2, all_symp_pr) if len(sym2) != 0 else (0, [])
                request.session['SSY'] = [sym2, sim2, psym2]
                request.session['step'] = "semantic"  # face semantic
                if sim2 == 1:
                    request.session['step'] = "RS2"  
                    response = related_sym(psym2)
                    if response != 0:
                        return JsonResponse({"response": response})

            if request.session['step'] == "RS2":
                temp = request.session['SSY']
                psym2 = temp[2]
                psym2 = psym2[int(s)]
                temp[2] = psym2
                request.session['SSY'] = temp
                request.session['step'] = "semantic"

            if request.session['step'] == "semantic":
                temp = request.session["FSY"] 
                sym1 = temp[0]
                sym2 = request.session['SSY'][0]
                # Here you can implement the logic to analyze the symptoms
                analysis_result = f"Based on your symptoms: {sym1} and {sym2}, we recommend you consult a healthcare professional."
                return JsonResponse({"response": analysis_result})

        return JsonResponse({"response": "Invalid request."})

    elif request.method == 'POST':
        if request.content_type == 'application/json':
            try:
                body_unicode = request.body.decode('utf-8')
                body_data = json.loads(body_unicode)
                user_message = body_data.get('message')
                print(f"Received POST message (JSON): {user_message}")  # Debugging line
            except json.JSONDecodeError:
                print("Failed to decode JSON")
                return JsonResponse({'response': "Invalid JSON received."})
        else:
            user_message = request.POST.get('message')
            print(f"Received POST message (Form Data): {user_message}")  # Debugging line

        if user_message:
            s = user_message.strip()  # Clean the input message
            if "step" in request.session:
                if request.session["step"] == "Q_C":
                    name = request.session["name"]
                    age = request.session["age"]
                    gender = request.session["gender"]
                    request.session.clear()
                    if s == "q":
                        return JsonResponse({"response": "Thank you for using our website, Mr/Ms " + name})

                if s.upper() == "OK":
                    return JsonResponse({"response": "What is your name?"})

                if 'name' not in request.session and 'step' not in request.session:
                    request.session['name'] = s
                    request.session['step'] = "age"
                    return JsonResponse({"response": "How old are you?"})

                if request.session["step"] == "age":
                    request.session["age"] = int(s)
                    request.session["step"] = "gender"
                    return JsonResponse({"response": "Can you specify your gender?"})

                if request.session["step"] == "gender":
                    request.session["gender"] = s
                    request.session["step"] = "Depart"

                if request.session['step'] == "Depart":
                    request.session['step'] = "BFS"
                    return JsonResponse({"response": f"Well, Hello again Mr/Ms {request.session['name']}, now I will be asking a few questions about your symptoms to see what you should do. Tap S to start diagnostic!"})

                if request.session['step'] == "BFS":
                    request.session['step'] = "FS"  # first symptom
                    return JsonResponse({"response": f"Can you specify your main symptom, Mr/Ms {request.session['name']}?"})

                if request.session['step'] == "FS":
                    sym1 = preprocess(s)
                    sim1, psym1 = syntactic_similarity(sym1, all_symp_pr)
                    request.session['FSY'] = [sym1, sim1, psym1]
                    request.session['step'] = "SS"  # second symptom
                    if sim1 == 1:
                        request.session['step'] = "RS1"  # related_sym1
                        response = related_sym(psym1)
                        if response != 0:
                            return JsonResponse({"response": response})
                    else:
                        return JsonResponse({"response": "You are probably facing another symptom. If so, can you specify it?"})

                if request.session['step'] == "RS1":
                    temp = request.session['FSY']
                    psym1 = temp[2]
                    psym1 = psym1[int(s)]
                    temp[2] = psym1
                    request.session['FSY'] = temp
                    request.session['step'] = 'SS'
                    return JsonResponse({"response": "You are probably facing another symptom. If so, can you specify it?"})

                if request.session['step'] == "SS":
                    sym2 = preprocess(s)
                    sim2, psym2 = syntactic_similarity(sym2, all_symp_pr) if len(sym2) != 0 else (0, [])
                    request.session['SSY'] = [sym2, sim2, psym2]
                    request.session['step'] = "semantic"  # face semantic
                    if sim2 == 1:
                        request.session['step'] = "RS2"  
                        response = related_sym(psym2)
                        if response != 0:
                            return JsonResponse({"response": response})

                if request.session['step'] == "RS2":
                    temp = request.session['SSY']
                    psym2 = temp[2]
                    psym2 = psym2[int(s)]
                    temp[2] = psym2
                    request.session['SSY'] = temp
                    request.session['step'] = "semantic"

                if request.session['step'] == "semantic":
                    temp = request.session["FSY"] 
                    sym1 = temp[0]
                    sym2 = request.session['SSY'][0]
                    analysis_result = f"Based on your symptoms: {sym1} and {sym2}, we recommend you consult a healthcare professional."
                    return JsonResponse({"response": analysis_result})

            return JsonResponse({"response": "Invalid request."})

        return JsonResponse({'response': "No message received."})