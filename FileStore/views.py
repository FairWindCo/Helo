from dal import autocomplete
from django import http
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
# Create your views here.
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from FileStore.forms import ProjectForm
from FileStore.models import Project, Tag


class ProjectAddFormView(View):
    def get(self, request):
        return render(request, 'FileStore/UpdateProject.html')


class ProjectList(ListView):
    model = Project


class ProjectCreate(CreateView):
    model = Project
    # fields = ['name', 'comments', 'tags']
    form_class = ProjectForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProjectCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form_object = form.save(commit=False)
        form_object.create_user = self.request.user
        form_object.update_user = self.request.user
        form_object.save()
        form_object.save_m2m()
        return http.HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'СОЗДАНИЕ ПРОЕКТА'
        return context


class ProjectUpdate(UpdateView):
    model = Project
    form_class = ProjectForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProjectUpdate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form_object = form.save(commit=False)
        form_object.update_user = self.request.user
        form_object.save()
        form.save_m2m()
        return http.HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'ИЗМЕНЕНИЕ ПРОЕКТА'
        return context


class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('projects-list')


class TagsAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Tag.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
