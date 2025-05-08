from django.contrib import admin
from .models import ChatSession, ChatMessage

class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ('sender', 'content', 'timestamp')

class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('id', 'user__email')
    inlines = [ChatMessageInline]
    readonly_fields = ('id',)

class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('session', 'sender', 'short_content', 'timestamp')
    list_filter = ('sender', 'timestamp')
    search_fields = ('content', 'session__id', 'session__user__email')
    
    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Content'

admin.site.register(ChatSession, ChatSessionAdmin)
admin.site.register(ChatMessage, ChatMessageAdmin)
