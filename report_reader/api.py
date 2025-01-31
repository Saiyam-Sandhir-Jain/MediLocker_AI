from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .views import extract_text_from_pdf, parse_lab_report, analyze_results
import json
import os
from django.conf import settings

class ReportReaderAPI(APIView):
    def post(self, request):
        uploaded_file = request.FILES.get('file')
        gender = request.data.get('gender', 'Female')

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

                    return Response({
                        "status": "success",
                        "abnormal_metrics": abnormal_metrics
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "status": "error",
                        "message": "Reference ranges file not found."
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            finally:
                if os.path.exists(file_path):
                    os.remove(file_path)
        else:
            return Response({
                "status": "error",
                "message": "Invalid file type. Please upload a PDF."
            }, status=status.HTTP_400_BAD_REQUEST)