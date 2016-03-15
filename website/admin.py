from django.contrib import admin
from user.models import *

# Register your models here.

admin.site.register(InterviewDepartment)
admin.site.register(InterviewRegister)
admin.site.register(InterviewGroup)
admin.site.register(Interviewer)
admin.site.register(Interviewee)
admin.site.register(Boss)