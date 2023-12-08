from django.db import models

class Pattern(models.Model):
    pattern_url_a = models.URLField(null=False, blank=False)
    pattern_url_b = models.URLField(null=False, blank=False)
    pattern_preview = models.URLField(null=False, blank=False)
    label = models.CharField(max_length=64)