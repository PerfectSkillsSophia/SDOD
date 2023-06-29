from django.db import models
from django.db import models
from django.contrib.auth.models import User
from administration.models import Question
# Create your models here.

class videoAns(models.Model):
    ansId = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=255,null=True)
    assessment_name = models.CharField(max_length=300,null=True)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    identi = models.CharField(max_length=300,null=True,default="None")
    videoAns = models.FileField(upload_to='media',blank=True)
    trasnscript = models.CharField(max_length=10000,null=True)
    answer_accurecy = models.IntegerField(null=True,default=0)
    def __str__(self):
        return f"{self.user_name} - {self.question_id} - {self.videoAns} - {self.assessment_name}"

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.feedback_type
    
class submission_status(models.Model):
        user_name = models.CharField(max_length=255,null=True)
        assessment_name = models.CharField(max_length=300,null=True)
        identi = models.CharField(max_length=300,null=True,default="None")
        final_result = models.IntegerField(null=True,default=0)
        submissionstatus = models.BooleanField(default=False)
        def __str__(self):
            return f" User name :{self.user_name} - Assessment_Name :  {self.assessment_name} - submission status : {self.submissionstatus}- final_result : {self.final_result}"