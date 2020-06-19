from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
class audio_files(models.Model):
  user_mac=models.CharField(max_length=1000)
  file_au=CloudinaryField('video')    

  def __str__(self):
      return self.user_mac
  
  @classmethod
  def get_user_uploads(cls,user_mac):
    uploads=cls.objects.filter(user_mac__icontains=user_mac)
    return uploads
