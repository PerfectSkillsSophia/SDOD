from django.urls import path
from assessments.views import * 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('afterlogin/',afterlogin,name='afterlogin'),
    path('welcome/<slug:ass_name>/',welcomeScreen,name='welcome'),
    path('answer/',answer,name='answer'),
    path('answer/fileUpload/',fileUpload, name='fileUpload'),
    path('feedback/',feedback,name='feedback'),
    path('thankyou/',thankyou, name='thankyou'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



