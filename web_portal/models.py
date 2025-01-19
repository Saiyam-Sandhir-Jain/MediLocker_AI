import uuid
from django.db import models

class Feedback(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False    
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    service = models.CharField(
        max_length=50,
        choices=[
            ('web_portal', 'Web Portal'),
            ('chatbot', 'Chatbot'),
            ('report_reader', 'Report Reader'),
        ]
    )
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.name} on {self.service}"
