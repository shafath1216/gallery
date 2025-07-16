from django.shortcuts import render, redirect, get_object_or_404
from .models import Gallery
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import os
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST


@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')  # redirect to your login page or homepage



# View to delete an image
@login_required
def delete(request, id):
    if request.method == "POST":
        # Ensure the image belongs to the logged-in user
        image = get_object_or_404(Gallery, id=id, user=request.user)
        # Delete the image file from the filesystem if it exists
        if image.Image and os.path.isfile(image.Image.path):
            os.remove(image.Image.path)
        # Delete the image record from the database
        image.delete()
        return redirect('gallery')

# View to update (edit) an image's details
@login_required
def update(request, id):
    # Get the gallery item, ensuring it belongs to the user
    gallery_items = get_object_or_404(Gallery, id=id, user=request.user)
    
    if request.method == "POST":
        # Update title and caption
        gallery_items.Title = request.POST.get('title')
        gallery_items.Caption = request.POST.get('caption')
        # If a new image is uploaded, replace the existing one
        image = request.FILES.get('image')
        if image:
            gallery_items.Image = image
        gallery_items.save()
        return redirect('gallery')
    
    # Show the update form with existing item details
    return render(request, 'update.html', {"items": gallery_items})

# View to show the landing/home page (public page)
def landing(request):
    return render(request, 'home.html')

# View to show the user's gallery page (requires login)
@login_required
@never_cache
def home(request):
    # Get all images uploaded by the logged-in user
    gallery_items = request.user.galleries.all()
    return render(request, 'gallery.html', {'gallery_items': gallery_items})

# View to handle user signup
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Basic validation
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('signup')

        # Create a new user and log them in
        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        return redirect('gallery')  # Redirect to gallery page

    return render(request, 'signup.html')  # Show signup form

# View to handle user login
@never_cache  # Prevents browser from caching login page
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('gallery')  # Redirect to gallery page
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')  # Show login form

# View to handle image upload
@login_required
def upload_image(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        caption = request.POST.get('caption')
        image = request.FILES.get('image')

        if title and caption and image:
            # Create new gallery item tied to the logged-in user
            Gallery.objects.create(user=request.user, Title=title, Caption=caption, Image=image)
            return redirect('gallery')  # Redirect to gallery page

    return render(request, 'upload.html')  # Show image upload form
