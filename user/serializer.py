from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Interviewee, InterviewRegister, InterviewDepartment
from rest_framework.exceptions import ValidationError


class InterviewRegistrationSerializer(serializers.ModelSerializer):
    queueNumber = serializers.IntegerField(read_only=True)
    class Meta:
        model = InterviewRegister
        fields = ('id', 'department', 'queueNumber')

    def validate_department(self, value):
        q = self.context['request'].user
        dept = InterviewDepartment.objects.get(pk=self.initial_data['department'])
        try:
            q.interviewee.interviewRegister.get(department=value)
        except InterviewRegister.DoesNotExist:
            if len(q.interviewee.interviewRegister.filter(department__group=dept.group)) < dept.group.maxRegister:
                return value
            else:
                raise serializers.ValidationError('you reached the maximum department registration allowed for this Interview Group')
        raise serializers.ValidationError('registered to this already')

    def create(self, validated_data):
        print(validated_data)
        q = self.context['request'].user
        validated_data['interviewee'] = q.interviewee
        validated_data['queueNumber'] = validated_data['department'].queueLast + 1
        validated_data['status'] = 0
        validated_data['department'].queueLast += 1
        validated_data['department'].save()
        return super(InterviewRegistrationSerializer, self).create(validated_data)


class InterviewMainSerializer(serializers.ModelSerializer):
    queue = serializers.CharField(source='queueNumber')

    class Meta:
        model = InterviewRegister
        fields = ('id', 'queue', 'status', 'customAnswer', 'comment', 'score')


class InterviewCallSerializer(serializers.ModelSerializer):
    queue_number = serializers.CharField(source='queueNumber')
    matric = serializers.CharField(source='interviewee.matricNumber')
    name = serializers.CharField(source='interviewee.name')

    class Meta:
        model = InterviewRegister
        fields = ('id', 'queue_number', 'matric', 'name', 'status')


class InterviewAdminSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='id')
    queue = serializers.CharField(source='queueNumber')
    matric = serializers.CharField(source='interviewee.matricNumber')
    name = serializers.CharField(source='interviewee.name')

    class Meta:
        model = InterviewRegister
        fields = ('id', 'queue', 'matric', 'name', 'status', 'customAnswer', 'comment', 'score', 'url')

    def is_valid(self, raise_exception=False):

        assert not hasattr(self, 'restore_object'), (
            'Serializer `%s.%s` has old-style version 2 `.restore_object()` '
            'that is no longer compatible with REST framework 3. '
            'Use the new-style `.create()` and `.update()` methods instead.' %
            (self.__class__.__module__, self.__class__.__name__)
        )

        assert hasattr(self, 'initial_data'), (
            'Cannot call `.is_valid()` as no `data=` keyword argument was '
            'passed when instantiating the serializer instance.'
        )

        if not hasattr(self, '_validated_data'):
            try:
                self._validated_data = self.run_validation(self.initial_data)
            except ValidationError as exc:
                self._validated_data = {}
                self._errors = exc.detail
            else:
                self._errors = {}

        if self._errors and raise_exception:
            raise ValidationError(self.errors)

        return not bool(self._errors)

    def save(self, **kwargs):
        assert not hasattr(self, 'save_object'), (
            'Serializer `%s.%s` has old-style version 2 `.save_object()` '
            'that is no longer compatible with REST framework 3. '
            'Use the new-style `.create()` and `.update()` methods instead.' %
            (self.__class__.__module__, self.__class__.__name__)
        )

        assert hasattr(self, '_errors'), (
            'You must call `.is_valid()` before calling `.save()`.'
        )

        assert not self.errors, (
            'You cannot call `.save()` on a serializer with invalid data.'
        )

        # Guard against incorrect use of `serializer.save(commit=False)`
        assert 'commit' not in kwargs, (
            "'commit' is not a valid keyword argument to the 'save()' method. "
            "If you need to access data before committing to the database then "
            "inspect 'serializer.validated_data' instead. "
            "You can also pass additional keyword arguments to 'save()' if you "
            "need to set extra attributes on the saved model instance. "
            "For example: 'serializer.save(owner=request.user)'.'"
        )

        assert not hasattr(self, '_data'), (
            "You cannot call `.save()` after accessing `serializer.data`."
            "If you need to access data before committing to the database then "
            "inspect 'serializer.validated_data' instead. "
        )

        validated_data = dict(
            list(self.validated_data.items()) +
            list(kwargs.items())
        )

        if self.instance is not None:
            self.instance = self.update(self.instance, validated_data)
            assert self.instance is not None, (
                '`update()` did not return an object instance.'
            )
        else:
            self.instance = self.create(validated_data)
            assert self.instance is not None, (
                '`create()` did not return an object instance.'
            )

        return self.instance

class IntervieweeRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    password = serializers.CharField(source='user.password', write_only=True)

    class Meta:
        model = Interviewee
        fields = ('id', 'username', 'password', 'name', 'matricNumber', 'year', 'major', 'phone')

    def update(self, instance, validated_data):
        print(instance)
        if instance is not None:
            q = validated_data.pop('user', None)
            q.pop('username', None)
        interviewee = super(IntervieweeRegistrationSerializer, self).update(instance, validated_data)
        if 'password' in q:
            interviewee.user.set_password(q['password'])
            interviewee.user.save()
        return interviewee

    def create(self, validated_data):
        info = validated_data.pop('user')
        print(info)
        user = User.objects.create_user(username=info.get('username'), password=info.get('password'))
        validated_data['user'] = user
        return super(IntervieweeRegistrationSerializer, self).create(validated_data)

