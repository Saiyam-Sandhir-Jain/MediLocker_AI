from django.shortcuts import render
from .forms import FeedbackForm
from django.contrib import messages

def home(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            
            messages.success(request, "Thank you for your feedback!")
            return render(request, 'web_portal/home.html', {'form': form})
        else:
            messages.error(request, "There was an error with your submission.")
    else:
        form = FeedbackForm()

    return render(request, 'web_portal/home.html', {'form': form})

def research(request):
    return render(request, 'web_portal/research.html')

def about_us(request):
    contributors = [
        {"name": "Saiyam Jain", "linkedin": "https://www.linkedin.com/in/saiyam-sandhir/", "image": "https://media.licdn.com/dms/image/v2/D4D03AQE9KGm9oUxy5A/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1695010011474?e=1743033600&v=beta&t=xuGThznfYPeVDzSuH39uM90QWIKU1TRWZ9b0kDBgjQE"},
        {"name": "Swaroop Bhowmik", "linkedin": "https://www.linkedin.com/in/swaroop-bhowmik-8907b52a0/", "image": "https://media.licdn.com/dms/image/v2/D4D03AQGwqBmNj9DJIA/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1732633493001?e=1743033600&v=beta&t=94r_WFo-CoIJ8e3Ab6Ibi-cHYnXSpxZ04iMZaRG0X70"},
        {"name": "Dipanjan Choudhury", "linkedin": "https://www.linkedin.com/in/dipanjan-choudhury/", "image": "https://media.licdn.com/dms/image/v2/D4D03AQGJXlH3Dxs43w/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1692809275327?e=1743033600&v=beta&t=xw2MzOUCY7aM0bnW3pL5TPUJmzOdpQmClO3Ysm7cdWI"},
        {"name": "Sanjoli Guta", "linkedin": "https://www.linkedin.com/in/sanjoli-gupta-746416318/", "image": "https://cdn-icons-png.flaticon.com/128/10412/10412454.png"},
        {"name": "Mahima Pal", "linkedin": "https://www.linkedin.com/in/mahima-pal-39360627a/", "image": "https://media.licdn.com/dms/image/v2/D4D03AQG5MQvLjdZG3Q/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1708338020700?e=1743033600&v=beta&t=H-msSEby2aJJnKyKAZRgKPDRoSyja2SEmOjB9NLU7qQ"},
        {"name": "Dr. Rajit Nair", "linkedin": "https://www.linkedin.com/in/dr-rajit-nair-367475220/", "image": "https://media.licdn.com/dms/image/v2/C5603AQF9cqcW3gwvJQ/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1638180663525?e=1743033600&v=beta&t=e7O64JmQcfpk71y2-ZchIm4yWp3CGpfQVg3EcfO6s-w"},
    ]

    return render(request, 'web_portal/about_us.html', {'contributors': contributors})