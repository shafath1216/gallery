from django.shortcuts import render,redirect,get_object_or_404
from .models import Gallery
from django.contrib.auth import login,authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import os
from django.views.decorators.cache import never_cache
# Create your views here.
def delete(request,id):
        
        if request.method=="POST":
            image=get_object_or_404(Gallery,id=id,user=request.user)
            if image.Image and os.path.isfile(image.Image.path):
                os.remove(image.Image.path)
            image.delete()
            return redirect('gallery') 


def update(request,id):
   gallery_items=get_object_or_404(Gallery,id=id,user=request.user)
    
   if request.method=="POST":
       gallery_items.Title=request.POST.get('title')
       gallery_items.Caption=request.POST.get('caption')
       image=request.FILES.get('image')
       if(image):
        gallery_items.Image=image
       gallery_items.save()
       return redirect('gallery')  
   
   
   
   
   
   return render(request,'update.html',{"items":gallery_items})

def landing(request):

    return render (request,'home.html')

def home(request):
    gallery_items = request.user.galleries.all()
    return render(request, 'gallery.html', {'gallery_items': gallery_items})

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

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)  # Log the user in immediately
        return redirect('gallery')  # Or wherever you want to redirect

    return render(request, 'signup.html')     

@never_cache
def login_view(request):
  if request.method == 'POST':
      username = request.POST.get('username')
      password = request.POST.get('password')

      user = authenticate(request, username=username, password=password)

      if user is not None:
          login(request, user)
          return redirect('gallery')  # or wherever you want
      else:
          messages.error(request, "Invalid username or password.")
          return redirect('login')

  return render(request, 'login.html')
  

@login_required
def upload_image(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        caption = request.POST.get('caption')
        image = request.FILES.get('image')

        if title and caption and image:
            Gallery.objects.create(user=request.user, Title=title, Caption=caption, Image=image)
            return redirect('gallery')

    return render(request, 'upload.html')  