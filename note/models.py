from django.db import models
from django.contrib.auth.models import User

TITLE_CHARS_LIMIT = 500

class Note(models.Model):
    owner = models.ForeignKey(User)
    content = models.TextField(null=False)
    title = models.CharField(max_length=TITLE_CHARS_LIMIT, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_favorite = models.BooleanField(default=False)
