from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer


def Homepage(request):
     template = loader.get_template('index.html')
     return HttpResponse(template.render())

class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        
        if serializer.is_valid():
            return Response({
                "message": "register successfully",
                "is_register": True
            }, status=status.HTTP_200_OK)
        
        return Response({
            "message": "register failed",
            "is_register": False,
            "region": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)