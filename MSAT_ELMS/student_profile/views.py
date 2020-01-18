from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import StudentProfile
from elms_accounts.models import Students


class StudentProfileView(DetailView):
	model = StudentProfile
	context_object_name = 'profile'
	template_name = 'profile/student_profile.html'