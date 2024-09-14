from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Notification
from .forms import NotificationForm
from django.contrib.admin.models import LogEntry
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .forms import CrimeReportForm

from django.shortcuts import render, redirect
# Create your views here.
def home(request):
    unread_notifications = Notification.objects.filter(read=False).count()
    return render(request, 'index.html',{'unread_notifications': unread_notifications})

@login_required()
def report(request):
    if request.method == 'POST':
        form = CrimeReportForm(request.POST, request.FILES)
        if form.is_valid():
            crime_report = form.save(commit=False)
            crime_report.user = request.user
            crime_report.save()
            messages.success(request, 'Crime report submitted successfully.')
            return redirect('report')
    else:
        form = CrimeReportForm()
    unread_notifications = Notification.objects.filter(read=False).count()
    return render(request, 'report.html', {'form': form,'unread_notifications': unread_notifications})
def about(request):
    unread_notifications = Notification.objects.filter(read=False).count()
    return render(request, 'about.html',{'unread_notifications': unread_notifications})

def safety_tips(request):
    unread_notifications = Notification.objects.filter(read=False).count()
    return render(request, 'safety-tips.html',{'unread_notifications': unread_notifications})



def register(request):
    """
    Handles user registration.

    :param request: HTTP request.
    :return: Rendered registration page or redirects to registration page.
    """
    if request.method == 'POST':
        data = request.POST
        full_name = data.get("name")
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")

        user = User.objects.filter(username=username)

        if user.exists():
            messages.info(request, "username already Taken")
            return redirect("/register/")

        user_email = User.objects.filter(email=email)

        if user_email.exists():
            messages.info(request, "email already Taken")
            return redirect("/register/")

        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=full_name,
        )

        user.set_password(password)
        user.save()

        messages.info(request, "Account created successfully")

        return redirect("/register/")
    return render(request, 'register.html')


def user_login(request):
    """
    Handles user login.

    :param request: HTTP request.
    :return: Redirects to the home page or shows an error message.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('report')  # Redirect to the home page or any other desired page
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    return render(request, 'login.html')


@login_required
def view_profile(request):
    notifications = Notification.objects.filter(user=request.user)
    unread_notifications = notifications.filter(read=False).count()
    return render(request, 'view-profile.html', {'user': request.user,'unread_notifications': unread_notifications})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('view_profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'edit-profile.html', {'form': form})
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


def user_logout(request):
    """
    Handles user logout.

    :param request: HTTP request.
    :return: Redirects to the login page.
    """
    logout(request)
    return redirect('login')





@user_passes_test(lambda u: u.is_superuser)
def create_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notification was successfully created!')
            return redirect('create_notification')
    else:
        form = NotificationForm()
    return render(request, 'create_notification.html', {'form': form})

@login_required
def view_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    unread_notifications = notifications.filter(read=False).count()
    return render(request, 'view_notifications.html', {'notifications': notifications, 'unread_notifications': unread_notifications})
@login_required
def read_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.read = True
    notification.save()
    return redirect('notification_detail', notification_id=notification.id)

@login_required
def notification_detail(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    return render(request, 'notification_detail.html', {'notification': notification})