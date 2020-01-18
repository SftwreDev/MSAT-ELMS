from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView


class HomePageView(TemplateView):
	template_name = 'index.html'