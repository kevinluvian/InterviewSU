from django.db import models
from django.contrib.auth.models import User


class InterviewGroup(models.Model):
    name = models.CharField(max_length=50)
    maxRegister = models.IntegerField()
    closeSelection = models.IntegerField()


class InterviewDepartment(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    group = models.ForeignKey(InterviewGroup, related_name="department")
    queueNow = models.IntegerField(default=0)
    queueLast = models.IntegerField(default=0)
    customQuestion = models.CharField(max_length=1000, blank=True)
    # failMessage = models.TextField(max_length=2000, blank=True)
    # successMessage = models.TextField(max_length=2000, blank=True)


class Interviewee(models.Model):
    user = models.OneToOneField(User, related_name="interviewee")
    name = models.CharField(max_length=100)
    matricNumber = models.CharField(max_length=50)
    year = models.IntegerField()
    major = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)


class InterviewRegister(models.Model):
    interviewee = models.ForeignKey(Interviewee, related_name="interviewRegister")
    department = models.ForeignKey(InterviewDepartment, related_name="interviewee")
    queueNumber = models.IntegerField()
    status = models.IntegerField()
    customAnswer = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    score = models.IntegerField(default=0)
    lastAction = models.DateTimeField(auto_now=True)
    resultPending = models.IntegerField(default=0)
    resultFinal = models.IntegerField(default=0)


class Interviewer(models.Model):
    department = models.ForeignKey(InterviewDepartment, related_name="interviewer")
    code = models.CharField(max_length=50)
    status = models.IntegerField(default=0)
    statusDesc = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(User, related_name="interviewer")
    lastAction = models.DateTimeField(auto_now=True)


class Boss(models.Model):
    group = models.ForeignKey(InterviewGroup, related_name="boss")
