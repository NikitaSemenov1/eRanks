from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Student, Employer


class CreateStudentForm(UserCreationForm):
    class Meta:
        model = Student
        fields = {'username', 'email', 'password1', 'password2', 'name1', 'name2', 'name3', 'university', 'department', 'course'}


class CreateEmployerForm(UserCreationForm):
    class Meta:
        model = Employer
        fields = {'username', 'email', 'password1', 'password2', 'name1', 'name2', 'name3', 'organization', 'position'}


class UploadFileForm(forms.Form):
    file = forms.FileField()
