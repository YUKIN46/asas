from django.urls import path
from django.contrib import admin
from . import views  # Import views from the current app
from . views import home, RegisterView, VerifyOTPView, LoginView

urlpatterns = [
    path('home/', views.home, name='home'),  # Map root URL to home view
    path('contactus/', views.contactus, name='contactus'),  # Contact Us page
    path('aboutus/', views.aboutus, name='aboutus'),  
    path('privacy/', views.privacy, name='privacy'),  
    path('menu/', views.menu, name='menu'),  
    path('terms/', views.terms, name='terms'),  # Registration page
    path('login/', views.login_view, name='login'),
    path('FAQs/', views.FAQ, name='FAQ'),  # Verification page
    path('cart/', views.cart, name='cart'),  # Contact Us page
    path('payment/', views.payment, name='payment'),  # Contact Us page
    path('signup/', views.signup, name='signup'),   
    path('feedback/', views.feedback, name='feedback'),  # Contact Us page
    path('signup/', views.signup, name='signup'),  # Registration page
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),  # Verification page
    path('admi/', views.admi, name='admi'),  # Verification page
              
    path('admin/', admin.site.urls),  # Admin URL

]