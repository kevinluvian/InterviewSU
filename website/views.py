from django.shortcuts import render
from rest_framework import viewsets,mixins
from rest_framework import generics
from django.contrib.auth import *
from user.models import Interviewee
from user.serializer import InterviewRegistrationSerializer, IntervieweeRegistrationSerializer
from django.contrib.auth.models import User
from user.permissions import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer,AdminRenderer


class RegisterViewSet(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Interviewee.objects.all()
    serializer_class = InterviewRegistrationSerializer

    def get(self, request):
        return render(request, 'register.html', {'serializer': self.serializer_class, 'title': 'Register for Interview'})

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print(request.POST)
            return render(request, 'register.html', {'serializer': serializer, 'title': 'Register for Interview'})
        self.create(request, *args, **kwargs)
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        return render(request, 'success.html', {'message': 'Registration successful'})


class IntervieweeProfileViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    This viewset is for viewing the profile, and update the data inside it
    """
    queryset = Interviewee.objects.all()
    serializer_class = InterviewRegistrationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsIntervieweeHimself,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Interviewee.objects.all()
    serializer_class = IntervieweeRegistrationSerializer
    #permission_classes = (IsAnonymous,)
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, template_name='profile.html')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers, template_name='register.html')

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, template_name='profile.html')
    """

@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'interviewee': reverse('interviewee-list', request=request, format=format)
    })