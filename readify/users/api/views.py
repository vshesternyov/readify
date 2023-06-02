from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status


class TokenWithEmailObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            token = response.data['access']
            data = {'email': user.email, 'token': token}
            return Response(data, status=status.HTTP_200_OK)
        return response
