from django.db import models
from django.db import models
from django.contrib.auth.models import User
from administration.models import Question

# Create your models here
class submission_status(models.Model):
        user_name = models.CharField(max_length=255,null=True)
        assessment_name = models.CharField(max_length=300,null=True)
        identi = models.CharField(max_length=300,null=True,default="None")
        final_result = models.IntegerField(null=True,default=0)
        submissionstatus = models.BooleanField(default=False)
        result_generate = models.BooleanField(default=False)
        result_process = models.BooleanField(default=False)
        def __str__(self):
            return f" User name :{self.user_name} - Assessment_Name :  {self.assessment_name} - identi : {self.identi}"

class videoAns(models.Model):
    ansId = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=255,null=True)
    assessment_name = models.CharField(max_length=300,null=True)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    submission_status = models.ForeignKey(submission_status, on_delete=models.CASCADE, related_name='video_answers')
    identi = models.CharField(max_length=300,null=True,default="None")
    videoAns = models.FileField(upload_to='media',blank=True)
    trasnscript = models.CharField(max_length=10000,null=True)
    answer_accurecy = models.IntegerField(null=True,default=0)
    confidence=models.IntegerField(null=True,default=0)
    nervousness=models.IntegerField(null=True,default=0)
    neutral=models.IntegerField(null=True,default=0)
    

    def __str__(self):
        return f"{self.ansId} -{self.user_name}  - {self.assessment_name} -  {self.identi}"

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.feedback_type
    
