from django.urls import path
from response_evaluation.views import * 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',response_evaluation_select,name='response_evaluation_select'),
    path('response_evaluation_login',response_evaluation_login,name='response_evaluation_login'),
    path('response_evaluation_dashboard/',response_evaluation_dashboard,name='response_evaluation_dashboard'),
    path('response_evaluation_test_dshsboard/',response_evaluation_test_dashboard,name='response_evaluation_test_dasboard'),
    path('response_evaluation_test/',response_evaluation_test,name='response_evaluation_test'),
    path('Response_Evaluation_Assessment/',Response_Evaluation_Assessment,name='Response_Evaluation_Assessment'),
    path('response_evaluation_test/fileUpload/',fileUpload, name='fileUpload'),
    path('response_evaluation_dshsboard/re_result_view/<str:test_code>/',re_result_view, name='re_result_view'),
    path('response_evaluation_result/<str:test_code>/',response_evaluation_result, name='response_evaluation_result'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



