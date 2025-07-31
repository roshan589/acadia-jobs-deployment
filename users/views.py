# Import necessary Django modules and decorators
from django.utils import timezone
import random
import string
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from .forms import PasswordResetRequestForm, SignupForm, VerificationCode
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib import messages
from functools import wraps
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.forms import SetPasswordForm
user = CustomUser()
today = timezone.now().date()


# Decorator to ensure only users with user_type 'faculty' can access the view
def faculty_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if hasattr(request.user, 'user_type') and request.user.user_type == "faculty":
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You do not have permission to access this page.")

    return wrapper


# Decorator to ensure only users with user_type 'student' can access the view
def student_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if hasattr(request.user, 'user_type') and request.user.user_type == "student":
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You do not have permission to access this page.")

    return wrapper


def faculty_parent_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if hasattr(request.user,
                   'user_type') and request.user.user_type == "parent" or request.user.user_type == "faculty":
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You do not have permission to access this page.")

    return wrapper


# User Signup View
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_char = email.split('@')[0][0]

            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
                return redirect('login')

            if not email.endswith('acadiau.ca'):
                form.add_error('email', "Only Acadia members can register.")
                return render(request, 'registration/signup.html', {'form': form})

            # Auto-detect user type
            if first_char.isdigit():
                user_type = 'student'
            elif first_char.isalpha():
                user_type = 'faculty'
            else:
                form.add_error('email', "Invalid Acadia email format.")
                return render(request, 'registration/signup.html', {'form': form})

            # Temporarily store user info in session
            request.session['signup_data'] = {
                'email': email,
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'user_type': user_type,
                'password': form.cleaned_data['password1'],  # Will be hashed later
            }

            # Generate a 6-digit code
            code = ''.join(random.choices(string.digits, k=6))
            request.session['verification_code'] = code

            # Send email
            send_mail(
                'Email Verification',
                f"Hi {form.cleaned_data['first_name']},\n\nPlease use this verification code to verify your account:\n\n{code}\n\nThanks!",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            messages.success(request, "Check your email for the verification code.")
            return redirect('verify_email')
    else:
        form = SignupForm()

    return render(request, 'registration/signup.html', {'form': form})


def verify_email(request):
    if request.method == 'POST':
        form = VerificationCode(request.POST)
        if form.is_valid():
            input_code = form.cleaned_data['verification_code']
            expected_code = request.session.get('verification_code')
            signup_data = request.session.get('signup_data')

            if input_code == expected_code and signup_data:
                # Final check just in case
                if CustomUser.objects.filter(email=signup_data['email']).exists():
                    messages.error(request, "This email is already registered.")
                    return redirect('login')

                # Create and save verified user
                user = CustomUser(
                    email=signup_data['email'],
                    first_name=signup_data['first_name'],
                    last_name=signup_data['last_name'],
                    user_type=signup_data['user_type'],
                    is_active=True,
                    is_verified=True,
                )
                user.password = make_password(signup_data['password'])  # Hash password
                user.save()

                # Cleanup session
                request.session.pop('signup_data', None)
                request.session.pop('verification_code', None)
                messages.success(request, "Your account has been verified. You can now log in.")
                return redirect('login')

            else:
                messages.error(request, "Invalid verification code.")
    else:
        form = VerificationCode()
    return render(request, 'registration/verifyEmail.html', {'form': form})


@login_required
def passChangeView(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = request.user

        if not user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
        elif new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
        elif len(new_password) < 8:
            messages.error(request, 'New password must be at least 8 characters long.')
        else:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Prevents logout
            messages.success(request, 'Your password was successfully changed.')
            return redirect('test')  # or any page you want

    return render(request, 'registration/passChange.html')


def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = CustomUser.objects.filter(email=email).first()  # use your CustomUser
            if user:
                token_generator = PasswordResetTokenGenerator()
                token = token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_url = request.build_absolute_uri(
                    reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                )

                send_mail(
                    subject="Password Reset Request",
                    message=(
                        f"Hi {user.first_name},\n\n"
                        f"To reset your password, click the link below:\n"
                        f"{reset_url}\n\n"
                        "If you didn’t request this, please ignore this email.\n\n"
                        "Thanks!"
                    ),
                    from_email="no-reply@yourdomain.com",  # Change to your sender email
                    recipient_list=[user.email],
                )
                messages.success(request, "Password reset email sent. Please check your inbox.")

                return redirect('password_email')
            else:
                messages.error(request, "No user found with this email.")
    else:
        form = PasswordResetRequestForm()

    return render(request, 'auth/passwordReset.html', {'form': form})


def password_email(request):
    return render(request, 'auth/passwordEmail.html')


def password_reset_confirm(request, uidb64, token):
    token_generator = PasswordResetTokenGenerator()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()  # saves new password
                messages.success(request, "Your password has been reset successfully.")
                return redirect('login')
        else:
            form = SetPasswordForm(user)

        return render(request, 'auth/passwordResetConfirm.html', {'form': form})
    else:
        messages.error(request, "The password reset link is invalid or expired.")
        return render(request, 'auth/passwordResetInvalid.html')

def logoutView(request):
    logout(request)
    return redirect('home')  # Redirect to home page after logout


