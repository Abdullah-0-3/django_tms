from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # created_by = 

    def __str__(self):
        return f"{self.name}"
