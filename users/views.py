from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from dairymanagementsystem.models import Animal, Farm
from dairymanagementsystem.views import farm_detail,add_farm,edit_farm,delete_farm,animal_add,animal_details,edit_animal,delete_animal,edit_animal_details,edit_farm_detail,add_milk_production,milk_detail

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("dairymanagementsystem:login"))
    else:
        farms = Farm.objects.all()
        animals = Animal.objects.all()
        return render(request, "index.html", {'farms': farms, 'animals': animals})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dairymanagementsystem:index.html')  # Redirect to the index page if authentication succeeds
        else:
            messages.error(request, "Wrong Credentials")
            return redirect('users:login')  # Redirect to the login page if authentication fails

    # If request method is not POST, render the login page
    return render(request, "login.html")

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        cpass = request.POST.get('confirm')
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        email = request.POST.get('Email')

        if password != cpass:
            messages.error(request, 'Passwords do not match.')
            return redirect('dairymanagementsystem:signup.html')

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('dairymanagementsystem:signup.html')

        # Create the user
        myUser = User.objects.create_user(username, email, password)
        myUser.first_name = fname
        myUser.last_name = lname
        myUser.save()
        
        messages.success(request, 'Your account has been created. Please log in.')
        return redirect('dairymanagementsystem:login')  # Redirect to the login page after successful registration

    # If request method is not POST, render the signup form template
    return render(request, 'users/signup.html')
