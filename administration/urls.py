from django.urls import path
from administration.views import * 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('dashboard/',dashboard,name='dashboard'),
    path('allAnswer/',allAnswer,name='allAnswer'),
    path('testresult/',testresult,name='testresult'),
    path('testresult/testresultfunc/',testresultfunc,name='testresultfunc'),
    path('run_task/', run_task, name='run_task'),
    path('addassessment/Add',Add_assessment,name='Add'),
    path('dashboard/assessment/<int:ass_id>/',view_assessments,name='view'),
    path('detail/<str:user_name>/<str:assessment_name>/<str:identi>/',detail_view, name='detail_view'),
    path('detail/<str:slug1>/<str:slug2>/<str:slug3>/result/', screenshot_to_pdf, name='screenshot_view'),
    path('addquestion/',Add_question,name='Addquestion'),
    path('addassessment',add_assessment,name='addassessment'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)