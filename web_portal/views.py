from django.shortcuts import render
from .forms import FeedbackForm

def home(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Process the data
            cleaned_data = form.cleaned_data
            print(cleaned_data)  # Example: Print data to console
            return render(request, 'web_portal/thank_you.html', {'name': cleaned_data['name']})
    else:
        form = FeedbackForm()

    return render(request, 'web_portal/home.html', {'form': form})

def research(request):
    return render(request, 'web_portal/research.html')

def about_us(request):
    return render(request, 'web_portal/about_us.html')