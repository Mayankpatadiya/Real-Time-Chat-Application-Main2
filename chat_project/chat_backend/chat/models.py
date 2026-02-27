from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        
        return self.user.username


class ChatGroup(models.Model):
    name = models.CharField(max_length=150, unique=True)
    members = models.ManyToManyField(UserProfile, related_name='groups', blank=True)
    created_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_groups')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Chat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_user2")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user1', 'user2'],
                name='unique_private_chat'
            )
        ]

    def __str__(self):
        return str(self.user1)

class Message(models.Model):
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name="messages",
        null=True,
        blank=True
    )
    group = models.ForeignKey(
        ChatGroup,
        on_delete=models.CASCADE,
        related_name="messages",
        null=True,
        blank=True
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )
    MESSAGE_TYPES = (
        ('text', 'Text'),
        ('image', 'Image'),
        ('file', 'File'),
    )
    content = models.TextField(blank=True, default='')
    file = models.FileField(upload_to='chat_files/%Y/%m/', blank=True, null=True)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default='text')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_image(self):
        if self.file:
            return self.file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'))
        return False

    @property
    def file_name(self):
        if self.file:
            import os
            return os.path.basename(self.file.name)
        return ''

    def __str__(self):
        return f"{self.sender}: {self.content[:20] if self.content else '[file]'}"
