from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Student, Listings
from .forms import SignupForm, Listing_Form
from django.db.models import Q

# Entry Page
def home(request):
    return render(request, 'home.html')

# Sign in Page
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

# Sign up Page    
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            # Create the User profile
            Student.objects.create(
                user=user,
                username=user.username,
                email=user.email
            )

            login(request, user)
            return redirect('dashboard')
    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})

# Main Page, from here must be logged in to see things
@login_required
def dashboard(request):
    query = request.GET.get("q", "")
    sort = request.GET.get("sort", "current")  # current | newest

    listings = Listings.objects.all()

    if query:
        listings = listings.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    if sort == "newest":
        listings = listings.order_by("-creation_Date")  # newest first
    else:
        listings = listings.order_by("creation_Date")   # current/oldest first

    return render(request, 'mainPage.html', {
        'listings': listings,
        'query': query,
        'sort': sort,
    })

@login_required
def toggle_bookmark(request, pk):
    listing = get_object_or_404(Listings, pk=pk)
    student = request.user.student

    if listing in student.bookmarks.all():
        student.bookmarks.remove(listing)
    else:
        student.bookmarks.add(listing)

    return redirect(request.META.get("HTTP_REFERER", "dashboard"))

@login_required
def bookmarks(request):
    student = request.user.student
    bookmarks = student.bookmarks.all()

    return render(request, "bookmarks.html", {
        "bookmarks": bookmarks
    })


# Send user back to sign in page
def logOut(request):
    logout(request)
    return redirect('signin')

# User profile
@login_required
def profile(request):
    student = request.user.student
    my_listings = student.listings.all()
    return render(request, 'profile.html', {
        "my_listings": my_listings
    })

#inbox user to user comm(will come soon)
@login_required
def inbox(request):
    return render(request, "inbox.html")


# Listing Creation
@login_required
def create_Listing(request):
    if request.method == "POST":
        form = Listing_Form(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user.student
            listing.save()
            return redirect('listing_confirmation')
    else:
        form = Listing_Form()

    return render(request, "create_listing.html", {"form": form})

# Confirmation page
@login_required
def listing_confirmation(request):
    return render(request, "listing_confirmation.html")

# Edit the listings block


@login_required
def edit_listing(request, pk):
    listing = get_object_or_404(Listings, pk=pk, user=request.user.student)

    if request.method == "POST":
        form = Listing_Form(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = Listing_Form(instance=listing)

    return render(request, 'edit_listing.html', {'form': form})


#Delete the listings block
@login_required
def delete_listing(request, pk):
    listing = get_object_or_404(Listings, pk=pk, user=request.user.student)

    if request.method == "POST":
        listing.delete()
        return redirect('profile')

    return render(request, 'delete_listing.html', {'listing': listing})

@login_required
def view_listing(request, pk):
    listing = get_object_or_404(Listings, pk=pk)
    return render(request, "view_listing.html", {"listing": listing})