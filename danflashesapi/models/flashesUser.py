from django.contrib.auth.models import User
from django.db import models

class FlashesUser(models.Model):
    flashes_name = models.CharField(max_length=64)
    profile_image_url = models.URLField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)