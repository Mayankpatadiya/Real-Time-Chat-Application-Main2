from django.contrib import admin
from .models import Chat, UserProfile, ChatGroup, Message

# Register your models here.
# admin.site.register(UserProfile)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display= ('id','user','profile_photo')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display= ('id','chat','group','sender','content')
    list_filter = ('chat', 'group','sender')
    search_fields = ('chat','group','sender')

@admin.register(ChatGroup)
class ChatGroupAdmin(admin.ModelAdmin):
    list_display= ('id','name','created_by','created_at')
    list_filter = ('name','members','created_by','created_at')
    search_fields = ('name','members')

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('user1','user2','created_at')
