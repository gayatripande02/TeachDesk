from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from studentapp.models import Student
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home_view(request):
    return render (request , 'studentapp/home.html')

def register_view(request):

    if request.method == 'POST':
        print(request.POST)
        un = request.POST.get('uname')
        em = request.POST.get('email')
        pwd = request.POST.get('pwd')

        if User.objects.filter(username=un).exists():
            print("User already exists...")
            return render (request , 'studentapp/register.html',{'error':'Username/password already exixts'})
        else:
            user = User.objects.create_user(username=un, email=em, password=pwd )
            print("User created successfully...")
            return redirect('login')

    return render (request , 'studentapp/register.html')

def login_view(request):
    print(request.POST)
    un = request.POST.get('uname')
    pwd = request.POST.get('pwd')

    user = authenticate(username = un , password = pwd)
    if user is not None:
        login(request,user)
        messages.success(request, "Login successful!")
        return redirect('home')    
    else:
        messages.error(request, "Invalid username or password!")

    return render (request , 'studentapp/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def create_view(request):
    if request.method == 'POST':
        print(request.POST)
        r = request.POST.get("roll")
        n = request.POST.get("nm")
        m = request.POST.get("marks")
        g = request.POST.get("gender")
        print(f"Student name is {n} and marks are {m}")
        obj = Student(roll = r , name = n , marks = m , gender = g)
        obj.save()
        print("Student saved successfully")
        return redirect("/studentapp/display/")


    return render (request , 'studentapp/create.html')

@login_required
def display_view(request):

    data = Student.objects.all()
    context = {"data" : data}

    return render (request, 'studentapp/display.html',context)

def delete_view(request,id):
    print ('in delete view',id)
    obj = Student.objects.get(pk=id)
    obj.delete()
    return redirect('display')

@login_required
def update_view(request,id):
    print ('in update view',id)
    obj = Student.objects.get(pk=id)
    
    if request.method == 'POST':
         i = request.POST.get("id")
         r = request.POST.get("roll")
         n = request.POST.get("nm")
         m = request.POST.get("marks")
         g = request.POST.get("gender")
         obj = Student.objects.get(pk = i)
         obj.roll = r
         obj.name = n
         obj.marks = m
         obj.gender = g
         obj.save()
         return redirect('display')

    return render(request,'studentapp/update.html',{'obj':obj})