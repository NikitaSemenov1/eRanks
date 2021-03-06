from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from .models import Student, Event, Employer
from .forms import CreateStudentForm, CreateEmployerForm, UploadFileForm
import os


def index(request):
    return render(request, "main/index.html", context={
        'student_count': Student.objects.count,
        'employer_count': Employer.objects.count
    })


@login_required(login_url='login')
def ranking_page(request):
    if hasattr(request.user, 'student'):
        return redirect('index')
    return render(request, "main/ranking.html", context={
        'students': Student.objects.all().order_by("-score")
    })


def handle_uploaded_file(f):
    with open('', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@login_required(login_url='login')
def upload_file(request):
    if not hasattr(request.user, 'student'):
        return redirect('index')
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            title = request.POST.get('event_title')
            event = Event(student=request.user.student, title=title)
            event.save()
            ext = os.path.splitext(str(request.FILES['file']))[1]
            destination = 'main/static/files/diploma_%s_%s%s' % (str(request.user.username), str(event.id), ext)

            for chunk in request.FILES['file'].chunks():
                open(destination, 'wb+').write(chunk)

            event.diploma = destination
            event.save()
        else:
            messages.error(request, form.errors)
    return redirect(reverse('profile', kwargs={'username': request.user.username}))


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
        'events': Event.objects.filter(is_denied=False, is_accepted=False).order_by('-id')
    })


def student_signup_page(request):
    if request.method == 'POST':
        form = CreateStudentForm(request.POST)
        if form.is_valid():
            messages.success(request, '???? ?????????????? ????????????????????????????????????')
            form.save()
            return redirect('student_signup')
        else:
            messages.error(request, form.errors)

    return render(request, "registration/student_signup.html")


def employer_signup_page(request):

    if request.method == 'POST':
        form = CreateEmployerForm(request.POST)
        if form.is_valid():
            messages.success(request, '???? ?????????????? ????????????????????????????????????')
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
            messages.info(request, '???????????????????????? ?????????? ?????? ????????????')
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
