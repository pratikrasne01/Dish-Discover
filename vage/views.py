from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url ='/')
def receipes(request):
    if request.method =="POST":
        data = request.POST
        
        receipe_ename = data.get('receipe_ename')
        receipe_description = data.get('receipe_description')
        receipe_image = request.FILES.get('receipe_image') 
        
        Receipe.objects.create(
            receipe_ename=receipe_ename,
            receipe_description=receipe_description,
            receipe_image=receipe_image,
        )
        
        return redirect('/receipes/')
    
    queryset = Receipe.objects.all()
    
    if request.GET.get('search'):
        queryset = queryset.filter(receipe_ename__icontains = request.GET.get('search'))
    
    context = {'receipes':queryset}
    
    return render(request, 'receipes.html', context)

@login_required(login_url ='/')
def update_receipe(request, id):
    queryset = Receipe.objects.get(id = id)
    
    if request.method == "POST":
        data = request.POST
        
        receipe_image = request.FILES.get('receipe_image')
        receipe_ename = data.get('receipe_ename')
        receipe_description = data.get('receipe_description')
        
        queryset.receipe_ename = receipe_ename
        queryset.receipe_description = receipe_description
        
        if receipe_image:
            queryset.receipe_image = receipe_image
            
        queryset.save()
        return redirect('/receipes/')
    
    context = {'receipe':queryset}
    return render(request, 'update-receipes.html', context)

@login_required(login_url ='/')
def delete_receipe(request, id):
    queryset = Receipe.objects.get(id = id)
    queryset.delete()
    return redirect('/receipes/')

def login_page(request):
    
    if request.method =="POST":
     
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username = username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('/')
        
        user = authenticate(username= username, password = password)
        
        if user is None:
            messages.error(request, 'Invalid Username or Password')
            return redirect('/')
        else:
            login(request, user)
            return redirect('/receipes/')
        
    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('/')
    

def register(request):
    
    if request.method =="POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = User.objects.filter(username = username)
        
        if user.exists():
            messages.error(request, 'Username Already Taken')
            return redirect('/register')
        
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username
        )
        
        user.set_password(password)
        user.save()
        
        messages.info(request, 'Account Created Successfully')
        
        return redirect('/register/')
        
    return render(request, 'register.html')