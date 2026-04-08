from django.urls import path
from users import views



urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('author/', views.add_author, name='add author')
]