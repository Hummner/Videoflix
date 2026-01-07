from rest_framework.views import APIView
from .serializers import RegisterSerializer
from rest_framework.response import Response
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import status

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
        
        return Response({"message": "Account successfully activated."}, status=status.HTTP_200_OK)
        