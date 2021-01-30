from django.urls import path, include
from .views import *

urlpatterns = [

    path('nlp_result/', NlpResultListView.as_view()),
    path('filter_malware/', FilterMalwareListView.as_view()),
    path('nlp_result_filtered/<str:value>/', NlpResultFilteredListView.as_view())

]