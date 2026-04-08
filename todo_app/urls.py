from django.urls import path
from .views import Todo



urlpatterns = [
    path('todos/', Todo.as_view(), name="todos"),
    path('todos/<int:id>/', Todo.as_view(),name="books_with_id" ),
    # path('endpoint/<int:id>/',  Todos.as_view(), name="books_with_id")
]