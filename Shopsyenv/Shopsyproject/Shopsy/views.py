from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import json
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from .models import Product
from .models import Order
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



@csrf_exempt
def create_order(request):
    """Creates an order"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON"}, status=400)

        user_id = data.get("user_id")
        product_id = data.get("product_id")
        quantity = data.get("quantity", 1)
        full_name = data.get("full_name")
        phone = data.get("phone")
        house_no = data.get("house_no")
        landmark = data.get("landmark", "")
        city = data.get("city")
        state = data.get("state")
        pincode = data.get("pincode")
        delivery_charge = data.get("delivery_charge", 50.00)

        errors = {}

        if not user_id or not User.objects.filter(id=user_id).exists():
            errors["user_id"] = "Invalid or missing user"

        if not product_id or not Product.objects.filter(id=product_id).exists():
            errors["product_id"] = "Invalid or missing product"

        if not full_name or len(full_name) < 3:
            errors["full_name"] = "Full name must be at least 3 characters long"

        if not phone or not phone.isdigit() or len(phone) < 10:
            errors["phone"] = "Invalid phone number"

        if not house_no:
            errors["house_no"] = "House number is required"

        if not city:
            errors["city"] = "City is required"

        if not state:
            errors["state"] = "State is required"

        if not pincode or len(pincode) < 6:
            errors["pincode"] = "Invalid pincode"

        if errors:
            return JsonResponse({"message": "Order creation failed", "errors": errors}, status=400)

        user = User.objects.get(id=user_id)
        product = Product.objects.get(id=product_id)

        order = Order(
            user=user,
            product=product,
            quantity=quantity,
            price=product.productprice,
            delivery_charge=delivery_charge,
            full_name=full_name,
            phone=phone,
            house_no=house_no,
            landmark=landmark,
            city=city,
            state=state,
            pincode=pincode
        )
        order.save()

        return JsonResponse({
            "message": "Order created successfully",
            "order_id": order.id,
            "total_price": order.total_price,
            "username": user.name,  # Send username
            "product_name": product.productname,  # Send product name
            "product_price": product.productprice,  # Send product price
            "order_date": order.order_date.strftime("%Y-%m-%d %H:%M:%S") 
        }, status=201)

    return JsonResponse({"message": "Method Not Allowed"}, status=405)


# @csrf_exempt
# def get_order_details(request, order_id):
#     """Retrieve details of a specific order"""
#     if request.method == "GET":
#         try:
#             order = Order.objects.get(id=order_id)
#             response_data = {
#                 "order_id": order.id,
#                 "user": order.user.username,
#                 "product": order.product.productname,
#                 "quantity": order.quantity,
#                 "price": str(order.price),
#                 "delivery_charge": str(order.delivery_charge),
#                 "total_price": str(order.total_price),
#                 "status": order.status,
#                 "order_date": order.order_date.strftime("%Y-%m-%d %H:%M:%S"),
#                 "full_name": order.full_name,
#                 "phone": order.phone,
#                 "house_no": order.house_no,
#                 "landmark": order.landmark,
#                 "city": order.city,
#                 "state": order.state,
#                 "pincode": order.pincode,
#             }
#             return JsonResponse(response_data, status=200)

#         except Order.DoesNotExist:
#             return JsonResponse({"message": "Order not found"}, status=404)

#     return JsonResponse({"message": "Method Not Allowed"}, status=405)