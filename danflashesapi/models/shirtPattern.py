from django.db import models

class ShirtPattern(models.Model):
    shirt = models.ForeignKey('Shirt', on_delete=models.CASCADE)
    pattern = models.ForeignKey('Pattern', on_delete=models.CASCADE)
    pattern_index = models.SmallIntegerField(null=True)