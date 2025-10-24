
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages

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