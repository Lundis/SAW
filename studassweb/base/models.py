from django.db import models
from solo.models import SingletonModel

class SiteConfiguration(SingletonModel):
    association_name = models.CharField(max_length=100, default='Site name')
