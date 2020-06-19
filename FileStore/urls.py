from django.contrib import admin
from django.urls import path, include

from FileStore.views import ProjectAddFormView

urlpatterns = [
    path('test', ProjectAddFormView.as_view()),
]