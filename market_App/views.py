from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import Listing_Form

def home(request):
    return render(request, 'home.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'signin.html')
    else:
        return render(request, 'signin.html')

@login_required
def dashboard(request):
    student = request.user.student
    listings = student.listings.all() 
    return render(request, 'mainPage.html', {
        'listings': listings
    })

def logOut(request):
    logout(request)
    return redirect('signin')

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def create_Listing(request):
    if request.method == "POST":
        form = Listing_Form(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user.student
            listing.save()
            return redirect('listing_confirmation')
    else:
        form = Listing_Form()

    return render(request, "create_listing.html", {"form": form})

@login_required
def listing_confirmation(request):
    return render(request, "listing_confirmation.html")