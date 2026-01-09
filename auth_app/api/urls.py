from django.urls import path
from .views import RegisterView, ActivateAccountView, LoginView, CustomTokenRefreshView, Logout, ConfirmNewPassword, ResetPassword

urlpatterns=[
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate-account'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', Logout.as_view(), name='logout'),
    path('password-reset/', ResetPassword.as_view(), name='password-reset'),
    path('password_confirm/<uidb64>/<token>/', ConfirmNewPassword.as_view(), name='password-confirm')

]