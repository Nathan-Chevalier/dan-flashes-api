from django.db import models

class ShirtFavorite(models.Model):
    shirt = models.ForeignKey("Shirt", on_delete=models.CASCADE, related_name='shirt_favorite')
    flashes_user = models.ForeignKey("FlashesUser", on_delete=models.CASCADE)