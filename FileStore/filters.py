import django_filters
from dal import autocomplete
from django.db import models

from FileStore.models import ProjectFile, Project, Tag, FileType


class FileFilter(django_filters.FilterSet):
    filename = django_filters.CharFilter(label='Имя файла содержит', lookup_expr='icontains')
    project = django_filters.ModelChoiceFilter(queryset=Project.objects.all(),
                                               widget=autocomplete.ModelSelect2(url='auto_project', attrs={
                                                   # Set some placeholder
                                                   'data-placeholder': 'Наберите начало тега ...',
                                                   # Only trigger autocompletion after 3 characters have been typed
                                                   'title': 'Проект'
                                               },
                                                                                ), )
    file_type = django_filters.ModelChoiceFilter(queryset=FileType.objects.all(),
                                                 widget=autocomplete.ModelSelect2(url='auto_types', attrs={
                                                     # Set some placeholder
                                                     'data-placeholder': 'Наберите начало тега ...',
                                                     # Only trigger autocompletion after 3 characters have been typed
                                                     'title': 'Типы файлов'
                                                 },
                                                                                  ), )
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(
            url='autocomlete_tags',
            attrs={
                # Set some placeholder
                'data-placeholder': 'Наберите начало тега ...',
                # Only trigger autocompletion after 3 characters have been typed
                'data-minimum-input-length': 3,
                'title': 'Теги'
            },
        ))


class Meta:
    model = ProjectFile
    fields = ['filename', 'project', 'file_type', 'tags']

    filter_overrides = {
        models.CharField: {
            'filter_class': django_filters.CharFilter,
            'extra': lambda f: {
                'lookup_expr': 'icontains',
            },
        },
    }
