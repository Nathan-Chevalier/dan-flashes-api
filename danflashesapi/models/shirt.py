from django.db import models
from django.contrib.auth.models import User

class Shirt(models.Model):
    flashes_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shirts_created")
    color = models.ForeignKey("Color", on_delete=models.CASCADE)
    label = models.CharField(max_length=64)
    public = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    patterns = models.ManyToManyField('Pattern', through='ShirtPattern')
    favorites = models.ManyToManyField('FlashesUser', through='ShirtFavorite')