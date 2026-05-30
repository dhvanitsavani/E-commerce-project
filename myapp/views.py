from django.shortcuts import render, redirect
from .models import User, Product
import random
import re
from django.core.mail import send_mail
from django.conf import settings
import os

products_list_ = [
    {
        'name': 'U.S. Polo Assn. Denim Co. Solid Regular Fit Track',
        'price': 2300,
        'description': 'Amplify your wardrobe with this pair of green regular fit trackpants from U.S. Polo Assn. Denim Co.. Tailored to sartorial perfection from premium quality fabric, it assures a soft and soothing touch against the skin.',
        'product_image': os.path.join(settings.MEDIA_ROOT, 'product-temp', 'product-7.webp'),
        'details': {
            'Color': 'Grass Green',
            'Fit': 'Regular',
            'Wash': 'Machine Wash',
            'Waist Rise': 'Mid Rise'
        },
        'available_no': 6000
    },
    {
        'name': 'U.S. Polo Assn. Solid Cotton Tapered Fit Men\'s Jeans',
        'price': 3100,
        'description': 'These solid jeans for men are shaped in the Brandon slim-tapered fit, offering a modern, casual silhouette with effortless everyday appeal.',
        'product_image': os.path.join(settings.MEDIA_ROOT, 'product-temp', 'product-8.webp'),
        'details': {
            'Color': 'Black',
            'Fit': 'Regular',
            'Length': 'Full',
            'Pattern': 'Solid',
            'Occasion': 'Casual',
            'Wash': 'Machine Wash',
            'Waist Rise': 'Mid Rise'
        },
        'available_no': 12000
    },
    {
        'name': 'U.S. Polo Assn. Harold Slim Straight Fit Blue Jeans',
        'price': 3400,
        'description': 'Casual solid jeans for men that blend comfort and style. Perfect for everyday wear and laid-back outings.',
        'product_image': os.path.join(settings.MEDIA_ROOT, 'product-temp', 'product-9.webp'),
        'details': {
            'Color': 'Navy Blue',
            'Fit': 'Regular',
            'Length': 'Regular',
            'Occasion': 'Casual',
            'Wash': 'Stone Wash',
            'Waist Rise': 'Mid Rise'
        },
        'available_no': 11000
    }
]

def is_valid_email(email):
    email_pattern = r'^\w+@\w+\.\w+\s*$'
    if re.match(email_pattern, email):
        return True
    else:
        return False

def add_products(request):
    try:
        for product in products_list_:
            Product.objects.create(
                seller = User.objects.get(email = 'savanidhvanit@gmail.com'),
                name = product['name'],
                price = product['price'],
                description = product['description'],
                product_image = product['product_image'],
                details = product['details'],
                available_no = product['available_no']
            )
        return render(request, 'index.html')
    except Exception as e:
        error_ = e
        return render(request, 'index.html', {'error_': error_})
    return redirect('index')

def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def signup(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(email = request.POST['email'])
            error_message = "Email already Registered"
        except:
            if request.POST['email'] != '' and request.POST['mobile'] != '' and request.POST['password'] != '':
                if is_valid_email(request.POST['email']):
                    if request.POST['password'] == request.POST['cpassword']:
                        if len(str(request.POST['password'])) >= 8:
                            User.objects.create(
                                name = request.POST['name'],
                                email = request.POST['email'],
                                mobile = request.POST['mobile'],
                                password = request.POST['password'],
                                age = request.POST['age'],
                            )
                            request.session['email'] = request.POST['email']
                            return redirect('index')
                        else:
                            error_message = "Create a Strong Password"
                    else:
                        error_message = "Password & Confirm Password are different"
                else:
                    error_message = "Enter a valid email"
            else:
                error_message = "All details are mendatory"
        return render(request, 'signup.html', {'error_message': error_message})
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(email = request.POST['email'])
            if request.POST['password'] == user.password:
                request.session['email'] = user.email
                request.session['profile_image'] = user.profile_image.url
                return redirect('index')
            else:
                error_message = "Incorrect Password"
        except:
            error_message = "Email is not Registered"
        return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def logout(request):
    try:
        del request.session['email']
    except:
        pass
    return redirect('index')

def forgot_password(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(email = request.POST['email'])
            otp = random.randint(1000, 9999)
            address = request.POST['email']
            subject = "Recovering ShopiGo account"
            message = f'Hello {user.name}, We\'re sending this email to verify it\'s you that requested for OTP and recover account on ShopiGo. Your OTP is {str(otp)} to recover your account and continue premium shopping again. Don\'t share this OTP with anyone, This OTP is time sensetive and wil expire after 5 minutes. If you face any kind of problem, kindly contact us on freefirebrandhub@gmail.com'
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [address,])
                request.session['otp'] = otp
                request.session['email_var'] = user.email
                return redirect('verify-otp')
            except:
                error_message = "Please Check your internet"
        except:
            error_message = "Email is not Registered"
        return render(request, 'forgot-password.html', {'error_message': error_message})
    return render(request, 'forgot-password.html')

def verify_otp(request):
    if request.method == 'POST':
        if int(request.POST['otp']) == request.session['otp']:
            return redirect('create-password')
        else:
            error_message = "Incorrect OTP"
        return render(request, 'verify-otp.html', {'error_message': error_message})
    return render(request, 'verify-otp.html')

def create_password(request):
    if request.method == 'POST':
        user = User.objects.get(email = request.session['email_var'])
        if request.POST['password'] == request.POST['cpassword']:
            if len(str(request.POST['password'])) >= 8:
                user.password = request.POST['password']
                user.save()
                del request.session['otp']
                del request.session['email_var']
                request.session['email'] = user.email
                return redirect('index')
            else:
                error_message = "Create a Strong Password"
        else:
            error_message = "Password & Confirm Password are different"

        return render(request, 'create-password.html', {'error_message': error_message})    

    return render(request, 'create-password.html')

def sell_products(request):
    return render(request, 'sell-products.html')