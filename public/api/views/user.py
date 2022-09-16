
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import response, status, views
from public.api.serializers.user import UserCompaniesSerializer

class UserCompaniesView(views.APIView):
    serializer_class = UserCompaniesSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            instance=request.user
        )
        print(serializer.data)
        return response.Response(serializer.data)