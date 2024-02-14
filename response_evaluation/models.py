from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class response_evaluation_Assessment(models.Model):
    user = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    def __str__(self):
        return self.title
    
    # models.py
class UserSubmittedQuestion(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    assessment = models.ForeignKey(response_evaluation_Assessment, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.question
