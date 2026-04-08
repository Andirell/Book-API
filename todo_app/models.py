from django.db import models

# Create your models here.
class Todos(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    author = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    