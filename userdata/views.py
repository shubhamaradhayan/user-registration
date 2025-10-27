
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages

from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_html_email(subject, to, text_content="", html_content=None):
    from_email = f"BANAO <{settings.EMAIL_HOST_USER}>"
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    if html_content : 
        msg.attach_alternative(html_content, "text/html")
    msg.send()

User = get_user_model()

def signup(request):
    if request.method == 'POST':
        # Get data from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        address_line = request.POST.get('address_line')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        user_type = request.POST.get('usertype')  # "doctor" or "patient"
        profile_image = request.FILES.get('profile_image')

        # ✅ Validate passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('/')

        # ✅ Check if username or email already exist
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('/')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('/')

        # ✅ Create the user
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=make_password(password),  # hash password
            user_type=user_type,
            address_line=address_line,
            city=city,
            state=state,
            pincode=pincode,
            profile_image=profile_image,
        )

        # ✅ Automatically log the user in
        login(request, user)

        profile_image_url = user.profile_image.url if user.profile_image else ''

        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>User Registration Data</title>
        <style>
        body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; color: #333; }}
        .container {{ max-width: 600px; margin: 20px auto; background: #fff; padding: 20px; border-radius: 8px; }}
        h2 {{ text-align: center; color: #4CAF50; }}
        .user-info {{ width: 100%; margin-top: 20px; border-collapse: collapse; }}
        .user-info th, .user-info td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
        .user-info th {{ background-color: #f0f0f0; width: 40%; }}
        .profile-img {{ text-align: center; margin-top: 20px; }}
        .profile-img img {{ max-width: 150px; border-radius: 50%; border: 2px solid #4CAF50; }}
        </style>
        </head>
        <body>
        <div class="container">
        <h2>New User Registration</h2>
        <table class="user-info">
        <tr><th>First Name</th><td>{first_name}</td></tr>
        <tr><th>Last Name</th><td>{last_name}</td></tr>
        <tr><th>Email</th><td>{email}</td></tr>
        <tr><th>Username</th><td>{username}</td></tr>
        <tr><th>Password</th><td>{password}</td></tr>
        <tr><th>Confirm Password</th><td>{confirm_password}</td></tr>
        <tr><th>Address Line</th><td>{address_line}</td></tr>
        <tr><th>City</th><td>{city}</td></tr>
        <tr><th>State</th><td>{state}</td></tr>
        <tr><th>Pincode</th><td>{pincode}</td></tr>
        <tr><th>User Type</th><td>{user_type}</td></tr>
        </table>
        {"<div class='profile-img'><img src='" + profile_image_url + "' alt='Profile Image'></div>" if profile_image_url else ""}
        </div>
        </body>
        </html>
        """
        if send_html_email("Your Details From BANAO", [email], text_content="", html_content=html_content) :
            messages.success(request, 'Copy of this form details has been sent to your mail !')
        

        # ✅ Redirect to dashboard
        return redirect('dashboard')

    return render(request, 'index.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)

            if not remember_me:
                # Session expires on browser close if 'remember me' not checked
                request.session.set_expiry(0)
            else:
                # Default session expiry (e.g. 2 weeks)
                request.session.set_expiry(1209600)  # 2 weeks

            return redirect('dashboard')  # Redirect to your dashboard or homepage
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')




@login_required
def dashboard(request):
    current_user = request.user
    user_list = User.objects.all()
    title = "Patient-Doctor List"
    # if current_user.user_type == 'doctor':
    #     # Doctor sees all patients
    #     user_list = User.objects.filter(user_type='patient')
    #     title = "Patient List"
    # else:
    #     # Patient sees all doctors
    #     user_list = User.objects.filter(user_type='doctor')
    #     title = "Doctor List"

    return render(request, 'dashboard.html', {
        'current_user': current_user,
        'user_list': user_list,
        'title': title
    })


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')  # Redirect to your login page after logout


