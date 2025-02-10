from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import json
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from .models import Product
from django.contrib.auth.hashers import check_password
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import SignupSerializer

# abhi123
#sdf2342j3h2jh3jjkajsdfassdfje

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
        
          # Check if user already exists
        if User.objects.filter(email=email).exists():
            return JsonResponse({"message": "Email already exists", "is_register": False}, status=400)

        if User.objects.filter(mobile=mobile).exists():
            return JsonResponse({"message": "Mobile number already registered", "is_register": False}, status=400)

        # Save user to database with hashed password
        user = User(name=name, email=email, mobile=mobile, password=password)
        user.save()
        
        return JsonResponse({"message": "Register successfully", "is_register": True}, status=200)

    return JsonResponse({"message": "Invalid request method"}, status=405)


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON"}, status=400)

        email = data.get('email')
        password = data.get('password')

        errors = {}

        if not email or email.strip() == "":
            errors["email"] = "Email cannot be blank"

        if not password or len(password) < 6:
            errors["password"] = "Invalid password details"

        if errors:
            return JsonResponse({"message": "Invalid input", "errors": errors}, status=400)

        # Check if user exists
        try:
            user = User.objects.get(email=email)
            if password==user.password:
                return JsonResponse({"message": "Login successful", "login": True}, status=200)
            else:
                return JsonResponse({"message": "Invalid email or password", "login": False}, status=401)
        except User.DoesNotExist:
            return JsonResponse({"message": "Invalid email or password", "login": False}, status=401)

    return JsonResponse({"message": "Invalid request"}, status=405)

@csrf_exempt
def product_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON"}, status=400)

        productname = data.get("productname")
        productprice = data.get("productprice")
        description = data.get("description")
        discount = data.get("discount")
        create_by = data.get("create_by")

        error = {}

        if not productname or productname.strip() == "":
            error["productname"] = "do not blank productname"

        if error:
            return JsonResponse({"is_product_create": False, "message": "product not created", "errors": error}, status=400)

        
        data = Product(productname=productname, productprice=productprice, description=description, discount=discount, create_by=create_by)
        data.save()

        return JsonResponse({"is_product_create": True, "message": "product created successfully"}, status=200)
    
    else:
        return JsonResponse({"message": "Method Not Allowed"},status=405)
    
    
@csrf_exempt
def get_product_view(request):
    """Retrieves all product details"""
    if request.method == "GET":
        products = Product.objects.all().values("id", "productname", "productprice", "description", "discount", "create_by","create_date")
        return JsonResponse({"products": list(products)}, status=200)

    return JsonResponse({"message": "Method Not Allowed"}, status=405)    

@csrf_exempt
def delete_product_view(request, product_id):
    """Deletes a product by its ID"""
    if request.method == "DELETE":
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            return JsonResponse({"is_deleted": True, "message": "Product deleted successfully"}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({"is_deleted": False, "message": "Product not found"}, status=404)

    return JsonResponse({"message": "Method Not Allowed"}, status=405)



@csrf_exempt
def update_product_view(request, product_id):
    """Updates a product by its ID"""
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON"}, status=400)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({"is_updated": False, "message": "Product not found"}, status=404)

        # Get updated fields from request
        productname = data.get("productname", product.productname)
        productprice = data.get("productprice", product.productprice)
        description = data.get("description", product.description)
        discount = data.get("discount", product.discount)
        create_by = data.get("create_by", product.create_by)

        # Update product details
        product.productname = productname
        product.productprice = productprice
        product.description = description
        product.discount = discount
        product.create_by = create_by
        product.save()

        return JsonResponse({"is_updated": True, "message": "Product updated successfully"}, status=200)

    return JsonResponse({"message": "Method Not Allowed"}, status=405)
