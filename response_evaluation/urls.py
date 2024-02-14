from django.urls import path
from response_evaluation.views import * 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',response_evaluation_login,name='response_evaluation_login'),
    path('response_evaluation_dashboard/',response_evaluation_dashboard,name='response_evaluation_dashboard'),
    path('Response_Evaluation_Assessment/',Response_Evaluation_Assessment,name='Response_Evaluation_Assessment'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



