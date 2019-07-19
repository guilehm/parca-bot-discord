from django.db import models
from django.contrib.postgres.fields import JSONField


class WakeUp(models.Model):
    data = JSONField(null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)
