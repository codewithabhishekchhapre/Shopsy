from django.urls import path
from . import views
from .views import SignupView

urlpatterns = [
     path("",views.Homepage),
     path('signup/', SignupView.as_view(), name='signup'),
]