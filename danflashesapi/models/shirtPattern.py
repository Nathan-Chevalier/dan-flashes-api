from django.db import models

class ShirtPattern(models.Model):
    shirt = models.ForeignKey('Shirt', on_delete=models.CASCADE, related_name='shirt_pattern')
    pattern = models.ForeignKey('Pattern', on_delete=models.CASCADE)
    pattern_index = models.SmallIntegerField(null=True)

    class Meta:
        unique_together = ('shirt', 'pattern_index')