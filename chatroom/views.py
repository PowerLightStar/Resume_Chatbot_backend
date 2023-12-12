# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny
# Create your views here.

import random, time
@api_view(['GET'])
@permission_classes([AllowAny])


def dashboard(request):
  
    return Response("Hello")


@api_view(['POST'])
@permission_classes([AllowAny])
def chatbot(request):
    msg = request.data['message']
    print(msg, "------------")
    username = request.user.username
    rand = random.randint(0, 100)
    response = f"Hi. I am {username}'s Interview Chatbot, would you like to ask me a question about my work history?" + str(rand)
  
    time.sleep(3)
    
        
    return Response({"message": response})
