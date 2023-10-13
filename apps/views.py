from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status 
from .serializers import (
    WriterSerializer, 
    TaskSerializer, 
    ProjectSerializer,
    userSerializer,
    LoginSerializer,
    CreateUserSerializer,
    UpdateUserSerializer,
    )
from rest_framework import status
from .models import(
    Writers, 
    Task,
    Project,
    RegisterUser,
)
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from knox import views as knox_views
from django.contrib.auth import login


#authentications

class CreateUserAPI(CreateAPIView):
    queryset = RegisterUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)

class ListUsersAPI(ListAPIView):
    queryset = RegisterUser.objects.all()
    serializer_class = userSerializer

class UpdateUserAPI(UpdateAPIView):
    queryset = RegisterUser.objects.all()
    serializer_class = UpdateUserSerializer

class LoginAPIView(knox_views.LoginView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)
            response =super().post(request, format=None)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(response.data, status=status.HTTP_200_OK)
        

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

#CRUD for tasks
@api_view(['GET', 'POST'])
def task_list(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def task_detail(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    
#CRUD for projects 
@api_view(['GET', 'POST']) 
def project_list(request):
    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(attachment=request.FILES.get('projects'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def project_detail(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
           new_attachment = request.data.get('attachment')
           if new_attachment:
               project.attachment.delete()
               project.attachment = new_attachment
           serializer.save(attachment=new_attachment)
           return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



       