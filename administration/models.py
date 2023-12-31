from django.db import models

class allAssessment(models.Model):
    assId = models.AutoField(primary_key=True)
    identi_assessment = models.CharField(max_length=300,null=True,default="None")
    assessmentName = models.CharField(max_length=255,null=True)
    assessmentType = models.CharField(max_length=255,null=True,default="None")
    assessmentDes = models.CharField(max_length=1000,null=True)
    def __str__(self):
        return self.assessmentName

class Question(models.Model):
    questionId = models.AutoField(primary_key=True)
    quostion= models.CharField(max_length=255,null=True)
    correctanswer = models.CharField(max_length=255,null=True)
    assessment = models.ForeignKey(allAssessment, on_delete=models.CASCADE)
    def __str__(self):
        return f" Question ID :{self.questionId} - Assessment_Name :  {self.assessment} - Question_Text : {self.quostion}"
    



    
