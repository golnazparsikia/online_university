from django.db import models

class status(models.TextChoices):
    ACTIVE ="active"
    PENDING = "pending"
    COMPLETED = "completed"
