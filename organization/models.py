from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'accounts.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='organizations'
    )

    def __str__(self):
        return f"{self.name} {self.created_by if self.created_by else 'No User'}"
