from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from handouts.models import Handouts

class HandoutsList(ListView):
    model = Handouts
    template_name = 'handouts/list_of_handouts.html'
    context_object_name = 'handouts_list'
