from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from member.serializers import UserSerializer, GroupSerializer, PersonalInfoSerializer
from .models import PersonalInfo

@api_view(['post'])
@permission_classes([AllowAny])
def Signup(request):
    serializer = UserSerializer(data=request.data)

    serializer.is_valid(raise_exception= True)
    
    user = serializer.save()
    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })
    
@api_view(["post"])
@permission_classes([AllowAny])
def Signin(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    else:
        return Response(
            {
                "error": "invalid credentials."
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

@api_view(['post'])
@permission_classes([AllowAny])
def Logout(request):
    response = Response()
    response.delete_cookie('jwt')
    response.status_code = status.HTTP_200_OK
    
    return response


class UserViewSet(viewsets.ModelViewSet):
    
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username = user)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

        
class GroupViewSet(viewsets.ModelViewSet):
    
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

class PersonalInfoViewSet(viewsets.ModelViewSet):
    queryset = PersonalInfo.objects.all()
    serializer_class = PersonalInfoSerializer
    
    permissions_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def create(self, request):
        tmp = request.data.copy()
        username = request.user.username
        tmp['username'] = username
        serializer = self.serializer_class(data = tmp, context ={'author': username} )
        
        if serializer.is_valid(raise_exception = True):
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status = status.HTTP_201_CREATED, headers = headers)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def list(self, request):
        if request.user.is_authenticated:
            queryset = PersonalInfo.objects.all()
            if request.user.is_staff:
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)
            else:
                username = request.user.username
                user_id = User.objects.get(username = username).id
                user = get_object_or_404(queryset, users = user_id)
                serializer = PersonalInfoSerializer(user)
                return Response(serializer.data)
        else:
            return Response(data={"error": "Please login first!"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def retrieve(self, request, pk = None):
        if request.user.is_authenticated:
            if request.user.is_staff:
                queryset = PersonalInfo.objects.all()
                if pk.isdigit():
                    user = get_object_or_404(queryset, users = pk)
                    serializer = PersonalInfoSerializer(user)
                    return Response(serializer.data)
                else:
                    return Response(data={"error": "Please check request form!"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data = {"error": "You haven't got permission to access other's data"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(data={"error": "Please login first!"}, status=status.HTTP_401_UNAUTHORIZED)