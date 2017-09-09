from datetime import datetime

# Django
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

# REST Framework
from rest_framework.response import Response
from rest_framework import status, generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter, SearchFilter
# Filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters

# Notes App
from note.filters import IsOwnerFilterBackend
from note.serializers import RegistrationSerializer
from note.serializers import NoteSerializer
from note.models import Note
from note.permissions import UserIsNoteOwnerOrStaff


class NoteFilter(filters.FilterSet):
    favorites = filters.BooleanFilter(name='is_favorite')
    title = filters.BaseInFilter(name='title')

    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'is_favorite', 'created_at', 'updated_at']

# todo add filters by title, content

class RegistrationView(APIView):
    """
    Allow registration of new users
    """
    permission_classes = ()

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        data = serializer.data

        user = User.objects.create(username=data['username'])
        user.set_password(data['password'])
        user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NoteList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    serializer_class = NoteSerializer

    permission_classes = (IsAuthenticated,)

    queryset = Note.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter, IsOwnerFilterBackend)
    filter_class = NoteFilter
    search_fields = ('^title', '^content')
    ordering_fields = ('updated_at',)
    ordering = ('updated_at',)

    def get(self, request, *args, **kwargs):
        """
        Get all user notes
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Adding a new note
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = serializer.data
            note = Note(owner=request.user, title=data['title'], content=data['content'])
            note.save()
            data['id'] = note.pk
            return Response(data, status=status.HTTP_201_CREATED)


class NoteDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):

    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthenticated, UserIsNoteOwnerOrStaff)

    def get(self, request, *args, **kwargs):
        """
        Get all user notes
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, pk):
        """
        Update a note
        """
        note = Note.objects.get(pk=pk)
        if note:
            note.updated_at = datetime.now()
            if 'is_favorite' in request.data:
                note.is_favorite = request.data['is_favorite']
            if 'title' in request.data:
                note.title = request.data['title']
            if 'content' in request.data:
                note.content = request.data['content']
            serializer = self.get_serializer(data=model_to_dict(note))
            if serializer.is_valid():
                note.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Note not found', status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        """
        Remove a note
        """
        return self.destroy(request, *args, **kwargs)
