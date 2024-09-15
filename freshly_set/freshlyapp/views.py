from django.shortcuts import render, redirect
from django.middleware.csrf import get_token
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseNotAllowed, JsonResponse
from .models import Product, Garden, Service, Blog
from .forms import ProductForm, ServiceRequestForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .forms import BlogForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.urls import reverse_lazy
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import generics, permissions
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.views import APIView
from .models import Blog, Comment, Like, Share, Poll, Vote, IDVerification
from django.db.models import Q
from rest_framework.generics import get_object_or_404
from .serializers import BlogSerializer, ProductSerializer, GardenSerializer, CommentSerializer,LikeSerializer, ShareSerializer,PollSerializer, VoteSerializer, IDVerificationSerializer
from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from django.contrib.auth import get_user_model, login, logout
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from rest_framework.validators import UniqueValidator
from .validators import custom_validation , validate_email, validate_password # Import your custom validation here
#csrf_protect_method = method_decorator(csrf_protect)
from django.utils import timezone

#imports for checkout

from django.contrib.auth.decorators import login_required
from .models import Cart, Order, OrderItem, Product

import random


from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer


# This is for typical django frontend html

from rest_framework import status
import logging

logger = logging.getLogger(__name__)

"""
class UserRegister(APIView):
    permission_classes =(permissions.AllowAny,)
    throttle_classes = []

    def post(self, request):
        clean_data = custom_validation(request.data)
        serializer = UserRegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(clean_data)
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
     permission_classes =(permissions.AllowAny,)
     authentication_classes=(SessionAuthentication,)
     throttle_classes = []

     def post(self, request):
         data = request.data
         assert validate_email(data)
         assert validate_password(data)
         serializer = UserLoginSerializer(data=data)
         if serializer.is_valid(raise_exception=True):
             user= serializer.check_user(data)
             login(request, user)
             return Response(serializer.data, status= status.HTTP_200_OK)

class UserView(APIView):
    permission_classes = (permissions,IsAuthenticated, )
    authentication_classes = (SessionAuthentication,)
    throttle_classes = []


    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'user':serializer.data}, status=status.HTTP_200_OK)

class UserLogout(APIView):
 throttle_classes = []

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
"""



def index(request):
    get_token(request)
    return render(request, 'index.html')
   
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')


    
@api_view(['GET'])
#class Blogs(APIView):
    #permission_classes = (AllowAny,)
    #authentication_classes = ()
    #@csrf_protect_method
@csrf_exempt
def blogs(request):
    if request.user.is_authenticated:
    #renderer_classes = [JSONRenderer]
        return render(request, 'blogs/BlogForm.jsx')


@login_required
def products(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('products')
    else:
        form = ProductForm()
    products = Product.objects.filter(user=request.user)
    return render(request, 'products.html', {'products': products, 'form': form})

@login_required
def services(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('services')
    else:
        form = ServiceRequestForm()
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services, 'form': form})

@login_required
def profile(request):
    return render(request, 'profile.html')


# The blog CRUD 
@csrf_exempt
def blog_list(request):
    if request.method == 'GET':
        blogs = Blog.objects.all()
        return render(request, 'blog_list.html', {'blogs': blogs})
    else:
        return HttpResponseNotAllowed(['GET'])
@csrf_exempt
def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    return render(request, 'blog_detail.html', {'blog': blog})

@api_view(['GET', 'POST'])
@csrf_exempt
@permission_classes([AllowAny])
def blog_create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blogs/BlogForm.jsx')
    else:
        form = BlogForm()
    return render(request, 'blogs/BlogForm.jsx', {'form': form})


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def blog_create(request):
    serializer = BlogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@csrf_exempt
def blog_update(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', slug=blog.slug)
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blogs/BlogForm.jsx', {'form': form})

def blog_delete(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if request.method == 'POST':
        blog.delete()
        return redirect('blog_list')
    return render(request, 'blog_confirm_delete.html', {'blog': blog})

# Implemented views for CRUD operations and like/share actions

class BlogListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def list(self, request, *args, **kwargs):
        logger.info(f"Request method: {request.method}")
        logger.info(f"Request data: {request.data}")
        return super().list(request, *args, **kwargs)


class BlogListCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]  # This allows unauthenticated access

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )
        return queryset
"""
    def blog_create(request):
        if request.method == 'POST':
            form = BlogForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('blogs/BlogForm.jsx')
        else:
            form = BlogForm()
        return render(request, 'blogs/BlogForm.jsx', {'form': form})
"""

    
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def Register(request):
    # Validate the input data
    serializer = UserRegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        # Check if the user already exists
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        if User.objects.filter(username=username).exists():
            return Response({"error": "This username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"error": "An account with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Save the user if validation passes
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Signup successful!",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    
    # Return errors if validation fails
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class BlogRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class LikeCreateAPIView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ShareCreateAPIView(generics.CreateAPIView):
    queryset = Share.objects.all()
    serializer_class = ShareSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'password_reset.html'
    form_class = PasswordResetForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return super().form_valid(form)
        else:
            messages.error(self.request, 'No user is associated with this email address.')
            return self.form_invalid(form)
        

# serialiser 
class GardenListCreateAPIView(generics.ListCreateAPIView):
    queryset = Garden.objects.all()
    serializer_class = GardenSerializer

class GardenRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Garden.objects.all()
    serializer_class = GardenSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class BlogViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'slug'

    def retrieve(self, request, slug=None):
        queryset = self.get_queryset()
        blog = get_object_or_404(queryset, slug=slug)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)
    
# query for blog articles 
"""
- The search_blog function handles HTTP GET requests to search for blog posts by title or content.
- If a query parameter q is provided, it filters the blog posts to include those where the title or
 content contains the query string.
- If no query is provided, it returns all blog posts.
- The result is returned as a JSON response with only the id, title, and content fields.
"""
@api_view(['GET'])
def search_blog(request):
    query = request.query_params.get('q', '')
    if query:
        blogs = Blog.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    else:
        blogs = Blog.objects.all()
    
    serializer = BlogSerializer(blogs, many=True)
    return Response(serializer.data)

# Polls 

class PollListCreateView(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class PollDetailView(generics.RetrieveAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class VoteCreateView(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        poll = get_object_or_404(Poll, pk=kwargs['pk'])
        choice = request.data.get('choice')
        
        if choice not in dict(Vote.CHOICES).keys():
            return Response({'error': 'Invalid choice'}, status=status.HTTP_400_BAD_REQUEST)
        
        vote, created = Vote.objects.update_or_create(
            poll=poll, user=request.user,
            defaults={'choice': choice}
        )

        if created:
            return Response({'status': 'Vote added'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'Vote updated'}, status=status.HTTP_200_OK)
        

# Verification photo and Id views
# install bot03
# to configure aws cli for face recogniotn.
class VerifyIDView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            verification = request.user.id_verification
            if verification.verify_user():
                return Response({"message": "User successfully verified."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Verification failed. ID or photo did not match."}, status=status.HTTP_400_BAD_REQUEST)
        except IDVerification.DoesNotExist:
            return Response({"error": "ID verification record not found."}, status=status.HTTP_404_NOT_FOUND)
        

class IDVerificationUpdateView(generics.UpdateAPIView):
    queryset = IDVerification.objects.all()
    serializer_class = IDVerificationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.id_verification

    def put(self, request, *args, **kwargs):
        verification_instance = self.get_object()
        serializer = self.get_serializer(verification_instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "User successfully verified."}, status=status.HTTP_200_OK)
    
class IDVerificationDetailView(generics.RetrieveAPIView):
    queryset = IDVerification.objects.all()
    serializer_class = IDVerificationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.id_verification
    


from .serializers import ProductSerializer


class CreateProduct(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RetrieveProduct(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)





class UpdateProduct(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class DeleteProduct(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework.pagination import PageNumberPagination


@permission_classes([AllowAny])
class ProductListView(APIView):
    def get(self, request, *args, **kwargs):
        # Filter products based on the search query parameter
        search_query = request.query_params.get('name')
        if search_query is not None:
            filtered_products = Product.objects.filter(name__icontains=search_query)
        else:
            filtered_products = Product.objects.all()

        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of items per page
        result_page = paginator.paginate_queryset(filtered_products, request)

        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    

#code for checkout
# views.py


@login_required(login_url='loginpage')
def checkout(request):
    # Fetch all cart items of the authenticated user
    raw_cart = Cart.objects.filter(user=request.user)
    
    # Validate the cart (e.g., check product quantity)
    for item in raw_cart:
        if item.product_qty > item.product.quantity:
            Cart.objects.filter(id=item.id).delete()
            messages.warning(request, f"Some products were removed due to insufficient stock.")
    
    # Calculate total price
    cart_items = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart_items:
        total_price += item.product.selling_price * item.product_qty

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    
    return render(request, 'store/checkout.html', context)

@login_required(login_url='loginpage')
def place_order(request):
    if request.method == 'POST':
        # Create a new order for the user
        new_order = Order(
            user=request.user,
            fname=request.POST.get('fname'),
            lname=request.POST.get('lname'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            country=request.POST.get('country'),
            pincode=request.POST.get('pincode'),
            payment_mode=request.POST.get('payment_mode'),
        )
        
        # Generate a tracking number for the order
        track_no = 'freshly' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=track_no).exists():
            track_no = 'freshly' + str(random.randint(1111111, 9999999))

        new_order.tracking_no = track_no
        new_order.total_price = calculate_cart_total(request)
        new_order.save()

        # Add all items from the user's cart to the order
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            OrderItem.objects.create(
                order=new_order,
                product=item.product,
                price=item.product.selling_price,
                quantity=item.product_qty
            )
            
            # Update product stock quantity
            product = Product.objects.get(id=item.product.id)
            product.quantity -= item.product_qty
            product.save()
        
        # Clear the user's cart after order placement
        Cart.objects.filter(user=request.user).delete()
        messages.success(request, "Your order has been placed successfully!")
        
        return redirect('home')
    else:
        return redirect('checkout')

def calculate_cart_total(request):
    """Helper function to calculate total cart price"""
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart:
        total_price += item.product.selling_price * item.product_qty
    return total_price

    



# Create a new order after checkout
@api_view(['POST'])
def create_order(request):
    try:
        # Extract cart items and other order data from request
        data = request.data
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # Log and return an error message
        print(f"Error creating order: {str(e)}")
        return Response({"error": "Failed to create order"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# View all orders for a user
@api_view(['GET'])
def my_orders(request):
    try:
        user_orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(user_orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"Error fetching orders: {str(e)}")
        return Response({"error": "Failed to fetch orders"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Cancel an order (allowed only if the status is 'out for shipping')
@api_view(['POST'])
def cancel_order(request, tracking_no):
    try:
        order = Order.objects.get(tracking_no=tracking_no, user=request.user)
        if order.status == 'out_for_shipping':
            order.status = 'cancelled'
            order.save()
            return Response({"message": "Order has been cancelled"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Cannot cancel order unless it is 'out for shipping'"}, status=status.HTTP_400_BAD_REQUEST)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Error cancelling order: {str(e)}")
        return Response({"error": "Failed to cancel order"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# View specific order details by tracking number
@api_view(['GET'])
def view_order(request, tracking_no):
    try:
        order = Order.objects.filter(tracking_no=tracking_no, user=request.user).first()
        if order:
            order_items = OrderItem.objects.filter(order=order)
            order_serializer = OrderSerializer(order)
            items_serializer = OrderItemSerializer(order_items, many=True)
            return Response({
                "order": order_serializer.data,
                "items": items_serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Error viewing order: {str(e)}")
        return Response({"error": "Failed to fetch order details"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


