from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.views import ObtainAuthToken


class AuthTokenUserIdAPIView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        credentials = {
            get_user_model().USERNAME_FIELD: request.data["username"],
            "password": request.data["password"],
        }
        user = authenticate(request=request, **credentials)
        response.data["user_id"] = user.id
        return response
