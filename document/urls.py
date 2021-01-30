from django.urls import path, include
from .views import *

urlpatterns = [

    path('nlp_result/', NlpResultListView.as_view())

]