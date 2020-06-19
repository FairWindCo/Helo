from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
# Create your views here.
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from FileStore.models import Project


class ProjectAddFormView(View):
    def get(self, request):
        return render(request, 'FileStore/UpdateProject.html')


class ProjectList(ListView):
    model = Project


class ProjectCreate(CreateView):
    model = Project
    fields = ['name']


class ProjectUpdate(UpdateView):
    model = Project
    fields = ['name']


class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('projects-list')
