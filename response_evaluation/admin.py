from django.contrib import admin
from response_evaluation.models import *


# Register your models here.
admin.site.register(UserSubmittedQuestion)
admin.site.register(response_evaluation_Assessment)
admin.site.register(re_recordings)
admin.site.register(UserSubmittedTest)

