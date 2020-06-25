from dal import autocomplete
from django import http
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
# Create your views here.
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormMixin
from django_tables2 import RequestConfig

from FileStore.filters import FileFilter
from FileStore.forms import ProjectForm, FileForm
from FileStore.models import Project, Tag, ProjectFile
from FileStore.tables import FilesTable
from mytemplates.views import FilterListDetailAjaxView


class AutoLoggingOperationMixin(FormMixin):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AutoLoggingOperationMixin, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form_object = form.save(commit=False)
        form_object.create_user = self.request.user
        form_object.update_user = self.request.user
        form_object.save()
        form.save_m2m()
        return http.HttpResponseRedirect(self.get_success_url())


class ProjectCreate(AutoLoggingOperationMixin, CreateView):
    model = Project
    form_class = ProjectForm
    extra_context = {'form_name': 'СОЗДАНИЕ ПРОЕКТА'}


class ProjectUpdate(AutoLoggingOperationMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    extra_context = {'form_name': 'ИЗМЕНЕНИЕ ПРОЕКТА'}


class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('projects-list')


class TagsAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Tag.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class FileUpdate(AutoLoggingOperationMixin, UpdateView):
    model = ProjectFile
    form_class = FileForm
    extra_context = {'form_name': 'ИЗМЕНЕНИЕ ФАЙЛА'}


class FileCreate(AutoLoggingOperationMixin, CreateView):
    model = ProjectFile
    form_class = FileForm
    extra_context = {'form_name': 'ИЗМЕНЕНИЕ ФАЙЛА'}


class ProjectList(ListView):
    model = Project


class FileList(ListView):
    model = ProjectFile


def projectfiles_table_view(request):
    return render(request, 'FileStore/projectfile_list.html')


def ajax_projectfiles_table_view(request):
    simple_table = FilesTable(ProjectFile.objects.all())
    RequestConfig(request).configure(simple_table)
    return HttpResponse(simple_table.as_html(request))


class FileTableView(FilterListDetailAjaxView):
    model = ProjectFile
    table_class = FilesTable
    template_name = 'FileStore/projectfile_list.html'
    filterset_class = FileFilter
    #create_filter = False