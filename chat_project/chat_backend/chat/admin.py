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
    search_fields = ('chat__user1__username', 'chat__user2__username', 'group__name', 'sender__username', 'content')

@admin.register(ChatGroup)
class ChatGroupAdmin(admin.ModelAdmin):
    list_display= ('id','name','created_by','created_at')
    list_filter = ('created_by','created_at')
    filter_horizontal = ('members',)
    search_fields = ('name', 'members__user__username', 'created_by__user__username')

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('user1','user2','created_at')
