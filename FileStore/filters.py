import django_filters
from dal import autocomplete
from django.db import models
from django.db.models import Q

from FileStore.models import ProjectFile, Project, Tag, FileType
from mytemplates.widgets import FlatPickerInput


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


class FileCompleteFilter(django_filters.FilterSet):
    filename = django_filters.CharFilter(label='Имя файла содержит', lookup_expr='icontains')
    file_type = django_filters.ModelChoiceFilter(queryset=FileType.objects.all(),
                                                 widget=autocomplete.ModelSelect2(url='auto_types', attrs={
                                                     # Set some placeholder
                                                     'data-placeholder': 'Наберите начало тега ...',
                                                     # Only trigger autocompletion after 3 characters have been typed
                                                     'title': 'Типы файлов'
                                                 },
                                                                                  ), )
    updated__gt = django_filters.DateFilter(field_name='updated', lookup_expr='gt',
                                              widget=FlatPickerInput(show_time=False))
    updated__lt = django_filters.DateFilter(field_name='updated', lookup_expr='lt',
                                              widget=FlatPickerInput(show_time=False))

    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        method='my_custom_filter',
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
        fields = ['filename', 'project', 'tags', 'updated']

    def my_custom_filter(self, queryset, name, value):
        print(name, value)
        return queryset.filter(Q(tags__in=value) | Q(project__tags__in=value))
