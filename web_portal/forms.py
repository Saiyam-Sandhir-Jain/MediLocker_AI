from django import forms

class FeedbackForm(forms.Form):
    name = forms.CharField(label="Your Name", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your name',
    }))
    email = forms.EmailField(label="Your Email", widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email',
    }))
    service = forms.ChoiceField(
        label="Service",
        choices=[
            ('web_portal', 'Web Portal'),
            ('chatbot', 'Chatbot'),
            ('report_reader', 'Report Reader'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    feedback = forms.CharField(label="Feedback", widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your feedback',
        'rows': 4,
    }))
