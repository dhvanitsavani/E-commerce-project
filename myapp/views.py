from django.shortcuts import render, redirect
from .models import User
import random
import re

def is_valid_email(email):
    email_pattern = r'^\w+@\w+\.\w+\s*$'
    if re.match(email_pattern, email):
        return True
    else:
        return False

def index(request):
    return render(request, 'index.html')

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
    return render(request, 'login.html')

def logout(request):
    try:
        del request.session['email']
    except:
        pass
    return redirect('index')