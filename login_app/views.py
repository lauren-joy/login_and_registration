from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            new_user = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'],
                password = hashed_pw,
            )
            request.session['user'] = new_user.id
            return redirect('/success')
    return redirect('/')

def login(request):
    if request.method == "POST":
        current_user = User.objects.filter(email=request.POST['email'])
        errors = User.objects.login_validator(request.POST)   
        if len(errors) > 0:
            for value in errors.items():
                messages.error(request, value)
            return redirect('/')
        if current_user:
            logged_user = current_user[0]
            request.session['user'] = logged_user.id
            return redirect('/success')
    else:
        return redirect ('/') 

def success(request):
    if 'user' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id = request.session['user'])
    }
    return render(request, 'success.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')