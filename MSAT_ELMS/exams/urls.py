from django.urls import path
from django.conf.urls import url

from . import views
from .views import ExamsTake

urlpatterns = [
	path('list-of-exams/', views.ExamsListView.as_view(), name='exams_list'),
	path('exams-detail/<str:slug>/', views.ExamsDetailView.as_view(), name='exams_detail'),
	url(regex=r'^(?P<exams_name>[\w-]+)/take/$',view=ExamsTake.as_view(), name='exams_question'),
]
