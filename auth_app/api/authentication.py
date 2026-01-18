from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication class.

    Authenticates users using the JWT access token
    stored in HTTP-only cookies instead of headers.
    """

    def authenticate(self, request):
        """
        Reads the access token from cookies,
        validates it, and returns the authenticated user.
        """

        raw_token = request.COOKIES.get("access_token")

        if not raw_token:
            return None

        validated_token = self.get_validated_token(raw_token)
        user = self.get_user(validated_token)

        return (user, validated_token)