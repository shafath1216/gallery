from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Gallery(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="galleries")
  Title= models.CharField(max_length=255)
  Image=models.ImageField(upload_to="gallery/")
  Caption=models.TextField(max_length=255)

  def __str__(self):
     return f'{self.Title} by {self.user.username}'  