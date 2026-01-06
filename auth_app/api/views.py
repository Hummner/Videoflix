from rest_framework.views import APIView
from .serializers import RegisterSerializer


class RegisterView(APIView):

    def post(self, request):
        serialiezer = RegisterSerializer(data=request.data)

        serialiezer.is_valid(raise_exception=True)
        user = serialiezer.save()

        self.send_activation_email(request, user)


    def send_activation_email(self, request, user):
        pass