from django.contrib.auth.models import User 

from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, WriterSerializer 
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login, logout 
from knox.views import LoginView as knoxLoginView 
from knox.views import LogoutView as knoxLogoutView
from rest_framework import status
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Writers 
from rest_framework.decorators import api_view


class UserList(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated,]



class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })
    
class LoginAPI(knoxLoginView):
   permission_classes = (permissions.AllowAny,)

   def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)

        success_message = f"{user.username} | logged in successfully."

        response_data = {
            "success" : True,
            "message" : success_message, 
            "user_id" : user.id
        }
        return Response(response_data, status=status.HTTP_200_OK)
        # return super(LoginAPI, self).post(request, format=None)

class LogoutAPI(knoxLogoutView):
    authentication_classes = [TokenAuthentication,]

    def post(self, request, format=None):
        logout(request)
        AuthToken.objects.filter(user=request.user).delete()
        return Response({"success" : "Logged out successfully"}, status=status.HTTP_200_OK)
        
#CRUD for writers
@api_view(['POST'])
def create_writer(request):
    serializer = WriterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_writers(request):
    writers = Writers.objects.all()
    serializer = WriterSerializer(writers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_writer(request, writer_id):
    try:
        writer = Writers.objects.get(pk=writer_id)
    except Writers.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = WriterSerializer(writer)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
def update_writer(request, writer_id):
    try:
        writer = Writers.objects.get(pk=writer_id)
    except Writers.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = WriterSerializer(writer, data=request.data, partial=True if request.method == 'PATCH' else False)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_writer(request, writer_id):
    try:
        writer = Writers.objects.get(pk=writer_id)
    except Writers.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    writer.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)




       