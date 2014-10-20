from django.db import models

from solo.models import SingletonModel

class InstallProgress(SingletonModel):
    """
    Keeps track of the installation progress
    """
    installed = models.BooleanField(default=False)
