from django.contrib import admin
from response_evaluation.models import *


# Register your models here.
admin.site.register(Category)
admin.site.register(Question)
admin.site.register(response_evaluation_Assessment)
admin.site.register(re_recordings)
admin.site.register(UserSubmittedTest)

