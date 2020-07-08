from dal import autocomplete
from django.urls import path, include

from FileStore.models import Tag, Project, FileType
from FileStore.views import ProjectDelete, ProjectUpdate, ProjectCreate, ProjectList, \
    TagsAutoComplete, FileList, FileCreate, FileUpdate, ajax_projectfiles_table_view, projectfiles_table_view, \
    FileTableView, ProjectFileDetail, get_file, FileSearchTableView, ajax_project_files_view, projects_views

urlpatterns = [
    path('project/add/', ProjectCreate.as_view(), name='project-add'),
    path('project/<int:pk>/', ProjectUpdate.as_view(), name='project-update'),
    path('project/<int:pk>/delete/', ProjectDelete.as_view(), name='project-delete'),
    path('projects/', ProjectList.as_view(), name='projects-list'),
    path('projects_/', projects_views, name='projects-list_'),


    path('file/add/', FileCreate.as_view(), name='file-add'),
    path('file/<int:pk>/update', FileUpdate.as_view(), name='file-update'),
    path('file/<int:pk>/delete/', ProjectDelete.as_view(), name='file-delete'),
    #path('files/', FileList.as_view(), name='files-list'),
    #path('files/', projectfiles_table_view, name='files-list'),
    path('files/', FileTableView.as_view(), name='files-list'),
    path('file/<int:pk>', ProjectFileDetail.as_view(), name='file-detail'),
    path('download/<int:pk>', get_file, name='download'),
    path('file/<int:pk>/ajax', ProjectFileDetail.as_view(template_name='FileStore/_file_detail.html'), name='file-detail-ajax'),
    path('search', FileSearchTableView.as_view(), name='search_files'),


    path('files-ajax/', ajax_projectfiles_table_view, name='files-list-ajax'),
    path('project-file-ajax/<int:id>', ajax_project_files_view, name='project-file-ajax'),


    path('autocomlete_tags', TagsAutoComplete.as_view(), name='autocomlete_tags'),
    path('auto_tags', autocomplete.Select2QuerySetView.as_view(
            model=Tag,
            create_field='name',
        ), name='auto_tags'),
    path('auto_project', autocomplete.Select2QuerySetView.as_view(
        model=Project,
        model_field_name='name',
    ), name='auto_project'),
    path('auto_types', autocomplete.Select2QuerySetView.as_view(
        model=FileType,
        model_field_name='name',
    ), name='auto_types'),
]