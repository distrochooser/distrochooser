from django.db import models


# See ADR-0036
class Violation(models.Model):
    user_agent = models.CharField(blank=False, null=False, max_length=500)
    reason = models.CharField(blank=False, null=False, max_length=500)
    hits = models.IntegerField(default=0, blank=False, null=False)
    last_hit = models.DateTimeField(default=None, blank=True, null=True)
    valid_until = models.DateField(default=None, blank=True, null=True)
    invalidated = models.BooleanField(default=False)
