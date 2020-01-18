from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView

from .forms import StudentSignUpForm, TeacherSignUpForm
from .models import User



class StudentSignUpView(CreateView):
	model = User
	form_class = StudentSignUpForm
	template_name = 'registration/signup_form.html'

	def get_context_data(self, **kwargs):
		kwargs['user_type'] = 'student'
		return super().get_context_data(**kwargs)

	def form_valid(self, form):
		user = form.save()
		login(self.request, user)
		return redirect('index')


class TeacherSignUpView(CreateView):
	model = User
	form_class = TeacherSignUpForm
	template_name = 'registration/signup_form.html'

	def get_context_data(Self, **kwargs):
		kwargs['user_type'] = 'teacher'
		return super().get_context_data(**kwargs)

	def form_valid(self, form):
		user = form.save()
		login(self.request, user)
		return redirect('index')


class SignUpView(TemplateView):
	template_name = 'registration/signup.html'


class LogOutView(TemplateView):
	template_name = 'registration/logout.html'