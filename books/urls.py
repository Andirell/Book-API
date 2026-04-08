from django.urls import path
from .views import Books



urlpatterns = [
    path('endpoint/', Books.as_view(), name="books"),
    path('endpoint/<int:id>/',  Books.as_view(), name="books_with_id")
]