

from django.urls import path,include
from .views import AnalysisView

urlpatterns = [
    path('getreport/', AnalysisView.as_view()),
]
