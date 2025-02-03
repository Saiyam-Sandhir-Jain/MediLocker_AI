from django.shortcuts import render
import pdfplumber
import json
import re
from PyPDF2 import PdfReader
from django.templatetags.static import static
import os
from django.conf import settings

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
    return text

def parse_lab_report(text, reference_ranges):
    metrics = {}
    for metric in reference_ranges:
        pattern = rf"{re.escape(metric)}\s*[:]?\s*([\d\.,]+)\s*(\w*)?"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                metrics[metric] = float(match.group(1)) 
            except ValueError:
                continue 
    return metrics

def analyze_results(metrics, reference_ranges, gender='Female'):
    abnormal_metrics = {}

    for metric, value in metrics.items():
        try:
            value = float(value)  
        except ValueError:
            pass 
        
        normalized_metric = normalize_metric_name(metric, reference_ranges)
        if normalized_metric:
            ranges = reference_ranges[normalized_metric]

            if isinstance(ranges, list) and isinstance(ranges[0], str):
                if value not in ranges:  
                    abnormal_metrics[metric] = {"value": value, "expected": ranges}
                continue

            if isinstance(ranges, dict) and gender in ranges:
                normal_range = ranges[gender]
            else:
                normal_range = ranges 

            if isinstance(normal_range, list) and len(normal_range) == 2:
                if value < normal_range[0]:
                    status = "Low"
                    link = f"https://www.ncbi.nlm.nih.gov/search/?term=Low+{normalized_metric}"
                elif value > normal_range[1]:
                    status = "High"
                    link = f"https://www.ncbi.nlm.nih.gov/search/?term=High+{normalized_metric}"
                else:
                    continue

                abnormal_metrics[metric] = {
                    'value': value,
                    'range': {'low': normal_range[0], 'high': normal_range[1]},
                    'status': status,
                    'link': link
                }

    return abnormal_metrics

def normalize_metric_name(metric, reference_ranges):
    for ref_metric in reference_ranges:
        aliases = reference_ranges.get(ref_metric, [])
        alias_strings = [alias.lower() for alias in aliases if isinstance(alias, str)]
        if metric.lower() in [ref_metric.lower()] + alias_strings:
            return ref_metric
    return None

def analyze(request):
    result = None
    abnormal_metrics = {}
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        gender = request.POST.get('gender', 'Female')
        
        if uploaded_file and uploaded_file.name.endswith('.pdf'):
            file_path = os.path.join(settings.MEDIA_ROOT, 'temp.pdf')
            
            with open(file_path, 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)

            try:
                text = extract_text_from_pdf(file_path)

                static_file_path = os.path.join(settings.STATIC_ROOT, 'report_reader', 'json', 'reference_ranges.json')

                if os.path.exists(static_file_path):
                    with open(static_file_path, 'r') as file:
                        reference_ranges = json.load(file)

                    metrics = parse_lab_report(text, reference_ranges)
                    abnormal_metrics = analyze_results(metrics, reference_ranges, gender)
                    result = True
                else:
                    raise FileNotFoundError(f"JSON file not found: {static_file_path}")
            finally:
                if os.path.exists(file_path):
                    os.remove(file_path)
        else:
            result = False
            abnormal_metrics = {"error": "Invalid file type. Please upload a PDF."}

    return render(request, 'reader.html', {'result': result, 'abnormal_metrics': abnormal_metrics})
