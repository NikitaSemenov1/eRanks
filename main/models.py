from django.db import models
from django.contrib.auth.models import User, UserManager


class Student(User):
    name1 = models.CharField(max_length=64, default='UNNAMED')
    name2 = models.CharField(max_length=64, default='UNNAMED')
    name3 = models.CharField(max_length=64, default='UNNAMED')
    score = models.IntegerField(default=0)
    university = models.CharField(max_length=64, default='NOINFO')
    department = models.CharField(max_length=64, default='NOINFO')
    course = models.IntegerField(default=1)

    def __str__(self):
        return self.get_short_name()

    def get_full_name(self):
        return "%s %s %s" % (self.name1, self.name2, self.name3)

    def get_short_name(self):
        return "%s %s. %s." % (self.name1, self.name2[0], self.name3[0])

    def get_study_info(self):
        return "%s курс, %s" % (self.course, self.university)

    def add_points(self, cost):
        self.score += cost
        self.save()


class Employer(User):
    name1 = models.CharField(max_length=64, default='Untitled')
    name2 = models.CharField(max_length=64, default='Untitled')
    name3 = models.CharField(max_length=64, default='Untitled')
    organization = models.CharField(max_length=64, default='Untitled')
    position = models.CharField(max_length=64, default='Untitled')

    def __str__(self):
        return self.get_short_name()

    def get_full_name(self):
        return "%s %s %s" % (self.name1, self.name2, self.name3)

    def get_short_name(self):
        return "%s %s. %s." % (self.name1, self.name2[0], self.name3[0])

    def get_organization_info(self):
        return "%s %s." % (self.position, self.organization)


class Event(models.Model):
    is_accepted = models.BooleanField(default=False)
    is_denied = models.BooleanField(default=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, default='VSEROS')
    cost = models.IntegerField(default=0)

    def accept(self):
        self.is_accepted = True
        self.save()

    def deny(self):
        self.is_denied = True
        self.save()

    def set_cost(self, cost):
        self.cost = cost
        self.save()

    def __str__(self):
        return "%s by %s" % (self.title, self.student.get_short_name())
