# Django
from django.contrib.auth.models import User

# REST Framework
from rest_framework import serializers

# Notes App
from note.models import Note


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'title', 'content', 'is_favorite', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at', 'id')