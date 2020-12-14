from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from rest_framework.generics import ListAPIView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from users.models import User
from users.serializer import UserSerializer
from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    

class LoginView(APIView):
            
    def post(self, request):
        
        email = request.data['email']
        password = request.data['password']
    
        try:
            user=User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            login(request, user)
            
        except Exception as e:
            raise e
            
        return Response(UserSerializer(user).data )



class ListUsersViews(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserView(APIView):
    serializer_class =UserSerializer

    def get_user(self, pk):
        try:
            user = User.objects.get(id= pk)
            return user
        except User.DoesNotExist:
            return


    def get(self, request, pk):
        if not self.get_user(pk):
            Response('user Not Found in database', status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(self.get_user(pk))
        return Response(serializer.data)
    
    def post(self, request):
        user=User.objects.create_user(email=request.data['email'], password=request.data['password'])
        #user.set_password(request.data['password'])
        #user.save()
        serializer =UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user= self.get_user(pk)
        serializer= UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, pk):
        user=User.objects.filter(id=pk)
        user.delete()
        return Response("user deleted",status=status.HTTP_204_NO_CONTENT)
   