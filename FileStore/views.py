from django.views import View
from django.shortcuts import render

# Create your views here.



class ProjectAddFormView(View):
    def get(self, request):
        return render(request, 'FileStore/UpdateProject.html')