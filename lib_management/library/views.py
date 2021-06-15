from django.shortcuts import render

# Create your views here.
def home_view(request, *args, **kwargs):
    print(request.user)
    return render(request, "index.html", {})

def search_book(request, *args, **kwargs):
    print(request.user)
    return render(request, "searchbook.html", {})

def admin_login(request, *args, **kwargs):
    print(request.user)
    return render(request, "adminlogin.html", {})

def BookAdd(request, *args, **kwargs):
        return render(request, "BookAdd.html", {})

def BookDelete(request, *args, **kwargs):
        return render(request, "BookDelete.html", {})

def CardAdd(request, *args, **kwargs):
        return render(request, "CardAdd.html", {})

def MemberAdd(request, *args, **kwargs):
        return render(request, "MemberAdd.html", {})