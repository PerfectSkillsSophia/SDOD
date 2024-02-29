from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    category_name = models.CharField(max_length=255)
    def __str__(self):
        return self.category_name

class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    question = models.CharField(max_length=300,null=True)
    def __str__(self):
        return self.question
# Create your models here.
class response_evaluation_Assessment(models.Model):
    user = models.CharField(max_length=255)
    assessment_code = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    questions = models.ManyToManyField(Question)
    def __str__(self):
        return self.title
class UserSubmittedTest(models.Model):

    created_by = models.CharField(max_length=300,null=True)
    Submitted_user_name = models.CharField(max_length=300,null=True)
    Submission_code = models.CharField(max_length=300,null=True)
    test_code = models.CharField(max_length=300,null=True)
    result_generate = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.Submitted_user_name}"

class re_recordings(models.Model):
    id =models.AutoField(primary_key=True)
    test = models.ForeignKey(UserSubmittedTest, on_delete=models.CASCADE, null=True, blank=True)
    Submission_code = models.CharField(max_length=300,null=True)
    que = models.CharField(max_length=300,null=True)
    videoAns = models.FileField(upload_to='media',blank=True)
    trasnscript = models.CharField(max_length=10000,null=True)
    confidence=models.IntegerField(null=True,default=0)
    nervousness=models.IntegerField(null=True,default=0)
    neutral=models.IntegerField(null=True,default=0)


    def __str__(self):
        return f"{self.test}"

