from dal import autocomplete
from django.contrib import admin
from django.urls import path, include

from FileStore.models import Tag
from FileStore.views import ProjectAddFormView, ProjectDelete, ProjectUpdate, ProjectCreate, ProjectList, \
    TagsAutoComplete

urlpatterns = [
    path('test', ProjectAddFormView.as_view()),
    path('project/add/', ProjectCreate.as_view(), name='project-add'),
    path('project/<int:pk>/', ProjectUpdate.as_view(), name='project-update'),
    path('project/<int:pk>/delete/', ProjectDelete.as_view(), name='project-delete'),
    path('projects/', ProjectList.as_view(), name='projects-list'),
    path('autocomlete_tags', TagsAutoComplete.as_view(), name='autocomlete_tags'),
    path('auto_tags', autocomplete.Select2QuerySetView.as_view(
            model=Tag,
            create_field='name',
        ), name='auto_tags'),
]