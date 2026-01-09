from rest_framework.views import APIView
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer, ResetPasswordSerializer
from rest_framework.response import Response
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken


class RegisterView(APIView):

    def post(self, request):
        serialiezer = RegisterSerializer(data=request.data)

        serialiezer.is_valid(raise_exception=True)
        user = serialiezer.save()

        activation_token = self.send_activation_email(request, user)

        data = {
                "user": {
                "id": user.id,
                "email": user.email
                },
                "token": activation_token
                }
        
        return Response(data)


    def send_activation_email(self, request, user):
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # activation_path = reverse(
        #     "activate-account",
        #      kwargs={"uidb64": uidb64, "token": token}
        # )

        activation_path = f"http://127.0.0.1:5500/pages/auth/activate.html?uid={uidb64}&token={token}"

        activation_url = request.build_absolute_uri(activation_path)

        subject = "Token Email"

        message= f"Hallo hier ist you token -> {activation_url}"

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )


        return token

class ActivateAccountView(APIView):
    

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({"detail": "The activation code is not valid."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not default_token_generator.check_token(user, token):
            return Response({"detail": "The activation link is expired or invalid."}, status=status.HTTP_400_BAD_REQUEST)
        
        user.is_active = True
        user.save(update_fields=['is_active'])
        print(user.is_active)
        
        return Response({"message": "Account successfully activated."}, status=status.HTTP_200_OK)
        

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        access_token = serializer.validated_data['access']
        refresh_token = serializer.validated_data['refresh']

        response = Response({'detail': 'Login successfull'}, status=status.HTTP_200_OK)

        response.set_cookie(
            key="access_token",
            value=access_token,
            secure=True,
            samesite='Lax'
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            secure=True,
            samesite='Lax'
        )

        return response
    
class CustomTokenRefreshView(TokenRefreshView):


    def post(self, request, *args, **kwargs):

        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None:
            return Response(
                {'message': 'Refresh Token is not found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data={'refresh': refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except (TokenError, InvalidToken):
            return Response(
                {'detail': 'Refresh token is invalid or expired'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        response = Response({
            "detail": "Token refreshed",
            "access": serializer.validated_data["access"]
            }, status=status.HTTP_200_OK)
        
        response.set_cookie(
            key="access_token",
            value=serializer.validated_data['access'],
            secure=True,
            samesite="Lax"
        )



        return response
    
class Logout(APIView):


    def post(self, request):

        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token is None:
            return Response(
                {'message': 'Refresh Token is not found'},
                status=status.HTTP_400_BAD_REQUEST
            )

        response = Response({"detail": "Logout successful! All tokens will be deleted. Refresh token is now invalid."}, status=status.HTTP_200_OK)

        response.delete_cookie(key="access_token")
        response.delete_cookie(key="refresh_token")

        return response
    

class ResetPassword(APIView):

    def post(self, request):

        serializer = ResetPasswordSerializer(data=request.data)

     
        if serializer.is_valid():
            self.send_reset_password_email(request, serializer.data['user'])

        return Response({"detail": "An email has been sent to reset your password."}, status=status.HTTP_200_OK)
    
    def send_reset_password_email(self, request, user):

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        reset_password_path = f"http://127.0.0.1:5500/pages/auth/forgot_password.html?uid={uidb64}&token={token}"
        reset_password_url = request.build_absolute_uri(reset_password_path)

        subject = "Reset your password"

        message = f"Here can you reset your password -> {reset_password_url}"

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL
            [user.email]
        )

class ConfirmNewPassword(APIView):


    def post(self, request):
        pass