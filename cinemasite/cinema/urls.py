from .views import *
from django.urls import path, include
urlpatterns = [
    path('', SessionsListView.as_view(), name='session_list'),
    path('login/', Login.as_view(), name = 'login'),
    path('register/', Register.as_view(), name = 'register'),
    path('logout/', Logout.as_view(), name = 'logout'),
    path('add_sessions/', SessionCreateView.as_view(), name = 'add_sessions'),
    path('update_sessions/<int:pk>/', UpdateProductView.as_view(), name = 'update_sessions'),
    path('create_halls/', HallsCreateView.as_view(), name = 'create_halls'),
    path('update_halls/<int:pk>/', UpdateHallsView.as_view(), name = 'update_halls'),
    path('movies/create_movies/', MoviesCreateView.as_view(), name = 'create_movies'),    
    path('movies/list_of_movies', MoviesListView.as_view(), name = 'list_of_movies'), 
    path('purchase_create/', ProductPurchaseView.as_view(), name = 'purchase_create'),
    path('list_of_purchases', ProductPurchaseListView.as_view(), name = 'list_of_purchases'),
]