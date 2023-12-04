from django.db import models

class ShirtFavorite(models.Model):
    shirt = models.ForeignKey("Shirt", on_delete=models.CASCADE)
    flashes_user = models.ForeignKey("FlashesUser", on_delete=models.CASCADE)