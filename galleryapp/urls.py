from django.urls import path,include
from .views import landing,signup,home,login_view,upload_image,delete,update
urlpatterns=[
 path('', landing, name='home'),              # Homepage
    path('signup/', signup, name='signup'),      # Manual signup
    path('gallery/', home, name='gallery'), 
     path('login/', login_view, name='login'), 
    path('upload/',upload_image, name='upload'),
     path('delete/<int:id>',delete, name='delete'),
    path('update/<int:id>',update,name='update')
]