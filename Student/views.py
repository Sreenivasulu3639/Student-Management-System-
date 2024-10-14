from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from Student.models import Student


# Create your views here.
@never_cache
def home(request):
    return render(request,"home.html")



@never_cache
def display_studs(request):
    students = Student.objects.all()
    data = {'students' : students}
    return render(request,"displaystudent.html",data)

@login_required
@never_cache
def add_studs(request):
    if request.method == 'GET':
        return render(request,"addstudent.html")
    else:
        student = Student()
        student.Name = request.POST["tbname"]
        student.Age = request.POST["tbage"]
        student.City = request.POST["tbcity"]
        student.Email = request.POST["tbemail"]
        student.Phone = request.POST["tbphone"]
        student.save()
        return redirect('displaystudents')

@login_required
def edit_studs(request,id):
    student = Student.objects.get(id=id)
    if request.method == 'GET':
        data = {"student":student}
        return render(request,"editstudent.html",data)

    else:
        student.Name = request.POST["tbname"]
        student.Age = request.POST["tbage"]
        student.City = request.POST["tbcity"]
        student.Email = request.POST["tbemail"]
        student.Phone = request.POST["tbphone"]
        student.save()
        return redirect('displaystudents')

@method_decorator(never_cache)
def delete_studs(request,id):
    student = Student.objects.get(id=id)
    student.delete()
    return redirect('displaystudents')

@never_cache
def login_fun(request):
    if request.method == 'GET':
        return render(request, "login.html")

    else:
        uname = request.POST["tbusername"]
        pword = request.POST["tbpass1"]
        user = authenticate(username=uname, password=pword)
        if user is not None:
            login(request, user)
            request.session['name'] = user.username
            return redirect("home")
        else:
            return redirect("login")

@never_cache
def register_fun(request):
    if request.method == 'GET':
        return render(request, "register.html")

    else:
        p1 = request.POST["tbpass1"]
        p2 = request.POST["tbpass2"]
        un = request.POST["tbusername"]
        em = request.POST["tbemail"]
        if p1 == p2:
            u = User.objects.create_superuser(un, em, p1)
            u.save()
            return redirect("login")
        else:
            return redirect('register')

@never_cache
def logout_fun(request):
    del request.session['name']
    logout(request)
    return redirect("login")