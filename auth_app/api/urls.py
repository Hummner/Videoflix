from django.urls import path
from .views import RegisterView, ActivateAccountView, LoginView

urlpatterns=[
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate-account'),
    path('login/', LoginView.as_view(), name='login')

]