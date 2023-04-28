from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=200)
    blog = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to='media/')
    add_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title