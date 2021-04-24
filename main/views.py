from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student, Event
from .forms import CreateStudentForm, CreateEmployerForm


def index(request):
    return render(request, "main/index.html")


def ranking_page(request):
    return render(request, "main/ranking.html", context={
        'students': Student.objects.all().order_by("-score")
    })


@login_required(login_url='login')
def event_management(request):
    if not request.user.is_staff:
        return redirect('ranking')
    if request.method == 'POST':
        if request.POST.get('Accept') is not None:
            cost = request.POST.get('cost')
            try:
                cost = int(cost)
            except ValueError:
                return redirect('event-management')
            event = Event.objects.get(id=request.POST.get('Accept'))
            event.set_cost(cost)
            event.accept()
            event.student.add_points(cost)
        if request.POST.get('Deny') is not None:
            Event.objects.get(id=request.POST.get('Deny')).deny()

    return render(request, "main/event_manager.html", context={
        'events': Event.objects.filter(is_denied=False, is_accepted=False)
    })


def student_signup_page(request):
    if request.method == 'POST':
        form = CreateStudentForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Вы успешно зарегистрировались')
            form.save()
            return redirect('student_signup')
        else:
            messages.error(request, form.errors)

    return render(request, "registration/student_signup.html")


def employer_signup_page(request):

    if request.method == 'POST':
        form = CreateEmployerForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Вы успешно зарегистрировались')
            form.save()
            return redirect('employer_signup')
        else:
            messages.error(request, form.errors)

    return render(request, "registration/employer_signup.html")


def login_page(request):
    if request.user.is_authenticated:
        return redirect('ranking')
    if request.method == 'POST':
        username = request.POST.get('user_name')
        password = request.POST.get('user_password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('ranking')
        else:
            messages.info(request, 'Неправильный логин или пароль')
    return render(request, 'registration/login.html')


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')


@login_required(login_url='login')
def profile(request, username):
    return render(request, 'main/profile.html', context={
        'events': Event.objects.filter(student__username=username, is_accepted=True),
        'username': username,
        'student': Student.objects.get(username=username)
    })
