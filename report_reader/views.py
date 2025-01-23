from django.shortcuts import render
import pymupdf
import json
import re

def extract_text_from_pdf(file_path):
    doc = pymupdf.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def parse_lab_report(text):
    metrics = {}
    lines = text.split('\n')
    for line in lines:
        if '*Hb' in line:
            match = re.search(r'Hb.*Female\s([\d\.]+)\s+gm', line)
            if match:
                metrics['Hemoglobin'] = float(match.group(1))
    return metrics

def analyze_results(metrics, reference_ranges, gender='Female'):
    abnormal_metrics = {}
    for metric, value in metrics.items():
        if metric in reference_ranges:
            ranges = reference_ranges[metric].get(gender, [])
            if ranges and not (ranges[0] <= value <= ranges[1]):
                abnormal_metrics[metric] = {
                    'value': value,
                    'range': {'low': ranges[0], 'high': ranges[1]}
                }
    return abnormal_metrics

def analyze(request):
    result = None
    abnormal_metrics = {}
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        gender = request.POST.get('gender', 'Female')
        if uploaded_file:
            with open('temp.pdf', 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
            text = extract_text_from_pdf('temp.pdf')
            metrics = parse_lab_report(text)
            with open('./reference_ranges.json', 'r') as file:
                reference_ranges = json.load(file)
            abnormal_metrics = analyze_results(metrics, reference_ranges, gender)
            result = True
    return render(request, 'reader.html', {'result': result, 'abnormal_metrics': abnormal_metrics})
