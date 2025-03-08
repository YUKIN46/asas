from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer
import random
import logging
# cms/views.py

from django.shortcuts import render

def home(request):
    return render(request, 'home.html')  # Render your home template
from .utils import send_otp_email
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')  

def aboutus(request):
    return render(request, 'aboutus.html')  
def contactus(request):
    return render(request, 'contactus.html')  
def home(request):
    return render(request, 'home.html')  

def menu(request):
    return render(request, 'menu.html')  
def privacy(request):
    return render(request, 'privacy.html')  
def terms(request):
    return render(request, 'terms.html')  

def FAQ(request):
    return render(request, 'FAQ.html')  
def contactus(request):
    return render(request, 'contactus.html')  

def login(request):
    return render(request, 'login.html')                

def cart(request):
    return render(request, 'cart2.html') 

def payment(request):                   
    return render(request, 'payment.html')  

def signup(request):
    return render(request, 'signup.html')   

def feedback(request):      
    return render(request, 'feedback.html')

def admi(request):      
    return render(request, 'admi.html')

logger = logging.getLogger(__name__)

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            otp = str(random.randint(100000, 999999))
            user = serializer.save(otp=otp, email_verified=False)
            send_otp_email(user.email, otp)
            return Response({'user_id': user.user_id}, status=status.HTTP_201_CREATED)
        logger.error(f"Registration failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        otp = request.data.get('otp')
        try:
            user = User.objects.get(user_id=user_id, otp=otp)
            user.email_verified = True
            user.save()
            return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            logger.error(f"Invalid OTP for user_id: {user_id}")
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return Response({'user_id': user.user_id}, status=status.HTTP_200_OK)
            else:
                logger.error(f"Invalid credentials for email: {email}")
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            logger.error(f"User not found for email: {email}")
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/home/')  # Redirect to the dashboard after login
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
import random
import json

@csrf_exempt
def send_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')

        # Generate OTP
        otp = str(random.randint(100000, 999999))

        # Save OTP to session (for verification)
        request.session['otp'] = otp
        request.session['email'] = email

        # Send OTP via email (you can use Django's email backend)
        # For now, just return the OTP for testing
        return JsonResponse({'otp': otp})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        profile_image = request.FILES.get('profile_image')

        # Check if email or username already exists
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already registered'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already taken'}, status=400)

        # Create user
        user = User(
            full_name=full_name,
            email=email,
            phone=phone,
            dob=dob,
            username=username,
            password=password,  # Hash the password in production
            profile_image=profile_image
        )
        user.save()

        return JsonResponse({'message': 'User registered successfully'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)