from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import json
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import SignupSerializer


def Homepage(request):
     template = loader.get_template('index.html')
     return HttpResponse(template.render())

# class SignupView(APIView):
#     def post(self, request):
#         serializer = SignupSerializer(data=request.data)
        
#         if serializer.is_valid():
#             return Response({
#                 "message": "register successfully",
#                 "is_register": True
#             }, status=status.HTTP_200_OK)
        
#         return Response({
#             "message": "register failed",
#             "is_register": False,
#             "region": serializer.errors
#         }, status=status.HTTP_400_BAD_REQUEST)




@csrf_exempt  # Disable CSRF for simplicity (not recommended for production)
def signup_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON request body
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON"}, status=400)

        # Extract fields
        email = data.get("email")
        mobile = data.get("mobile")
        name = data.get("name")
        password = data.get("password")

        # Basic validation
        errors = {}

        if not email or "@" not in email:
            errors["email"] = "Invalid email format"

        if not mobile or not mobile.isdigit() or len(mobile) < 10:
            errors["mobile"] = "Invalid mobile number"

        if not name or len(name) < 3:
            errors["name"] = "Name must be at least 3 characters long"

        if not password or not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{6,}$', password):
            errors["password"] = "Password must contain letters and numbers, min length 6"

        if errors:
            return JsonResponse({"message": "Register failed", "is_register": False, "errors": errors}, status=400)

        return JsonResponse({"message": "Register successfully", "is_register": True}, status=200)

    return JsonResponse({"message": "Invalid request method"}, status=405)
