from django.db import models
from users.models import Author


# Create your models here.
class Book(models.Model):
    BOOK_TYPE = (
        ("inclusive", "Inclusive"),
        ("exclusive", "Exclusive")
    )
    author = models.ForeignKey(Author, related_name="authors_book", null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=50)
    price = models.FloatField()
    book_type = models.CharField(max_length=9, choices=BOOK_TYPE, default="inclusive")
    published_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
