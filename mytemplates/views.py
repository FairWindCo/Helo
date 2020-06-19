from django.shortcuts import render

# Create your views here.
def show_test(request):
    return render(request, 'mytemplates/mytemplate.html')

def show_admin(request):
    return render(request, 'mytemplates/mybacktemplate.html')