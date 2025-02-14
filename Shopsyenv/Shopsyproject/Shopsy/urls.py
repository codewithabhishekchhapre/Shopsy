from django.urls import path
from . import views
# from .views import SignupView

urlpatterns = [
     path("",views.Homepage),
     path('upload/', views.upload_image, name='upload_image'),
     path('image-uploaded/', views.image_uploaded, name='image_uploaded'),
     
     
     path('signup/', views.signup_view, name='signup'),
     path('login/', views.login_view, name='login'),
     path('login_temp/', views.login_view_temp, name='login'),
     path('createProduct/', views.product_view, name='create_product'),
     path('getProduct/', views.get_product_view, name='get_product'),
     path('deleteProduct/<int:product_id>/', views.delete_product_view, name='delete_product'),
     path('updateProduct/<int:product_id>/', views.update_product_view, name='update_product'),
     path('create-order/', views.create_order, name='create-order'),
     path('generate-otp/',views.generate_otp),
     path('verify-otp/',views.verify_otp)
]