from django.urls import path
from . import views
# from .views import SignupView

urlpatterns = [
     path("",views.Homepage),
     path('signup/', views.signup_view, name='signup'),
     path('login/', views.login_view, name='login'),
     path('createProduct/', views.product_view, name='create_product'),
     path('getProduct/', views.get_product_view, name='get_product'),
     path('deleteProduct/<int:product_id>/', views.delete_product_view, name='delete_product'),
     path('updateProduct/<int:product_id>/', views.update_product_view, name='update_product'),
      path('create-order/', views.create_order, name='create-order')
]