"""interview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from website import views
from interviewer1.views import InterviewAdminViewSet
from rest_framework.routers import DefaultRouter,SimpleRouter

router = DefaultRouter()
router.register(r'user', views.IntervieweeViewSet)
router.register(r'register', views.InterviewRegisterViewSet)
router.register(r'admin', InterviewAdminViewSet)
router.register(r'judge', views.InterviewAdminJudgeViewSet)
print(router.urls)
print(dir(router))
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^tes/', views.InterviewAdminView.as_view()),
    url(r'^tes2/', views.hello_world),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]