from cinema.API.resources import HallViewSet, SessionsViewSet, PurchaseViewSet, MovieViewSet
from .views import SessionsListView, Login, Register, Logout, SessionCreateView, UpdateProductView,\
                    HallsCreateView, UpdateHallsView, MoviesCreateView, MoviesListView, ProductPurchaseListView
from rest_framework.routers import SimpleRouter
from django.urls import path, include
from rest_framework.authtoken import views

router = SimpleRouter()
router.register(r'halls', HallViewSet)
router.register(r'sessions', SessionsViewSet)
router.register(r'purchases', PurchaseViewSet)
router.register(r'movies', MovieViewSet)
# router.register(r'returns', AdminReturnViewSet)


urlpatterns = [
    path('', SessionsListView.as_view(), name='session_list'),
    path('login/', Login.as_view(), name = 'login'),
    path('register/', Register.as_view(), name = 'register'),
    path('logout/', Logout.as_view(), name = 'logout'),
    path('create_sessions/', SessionCreateView.as_view(), name = 'create_sessions'),
    path('update_sessions/<int:pk>/', UpdateProductView.as_view(), name = 'update_sessions'),
    path('create_halls/', HallsCreateView.as_view(), name = 'create_halls'),
    path('update_halls/<int:pk>/', UpdateHallsView.as_view(), name = 'update_halls'),
    path('movies/create_movies/', MoviesCreateView.as_view(), name = 'create_movies'),    
    path('movies/list_of_movies', MoviesListView.as_view(), name = 'list_of_movies'), 
    path('purchase_create/', MoviesListView.as_view(), name = 'purchase_create'),
    path('list_of_purchases', ProductPurchaseListView.as_view(), name = 'list_of_purchases'),
    path('api/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
]