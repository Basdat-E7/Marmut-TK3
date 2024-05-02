from django.shortcuts import render

# Create your views here.
def show_main(request):
    
    return render(request, "dashboard.html")

def login(request):

    return render(request, "login.html")

def register(request):
    return render(request, "register.html")

def register_user(request):
    return render(request, "register_user.html")

def register_label(request):
    return render(request, "register_label.html")