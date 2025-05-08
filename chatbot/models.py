from django.db import models
from django.conf import settings
import uuid
import json
from datetime import datetime

class ChatSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    chat_history = models.JSONField(default=list, blank=True)
    
    def __str__(self):
        return f"Chat {self.id} - {self.user.email if self.user else 'Anonymous'}"
    
    def get_recent_messages(self, count=5):
        messages = self.messages.all().order_by('-timestamp')[:count]
        return [
            {
                'content': msg.content,
                'sender': msg.sender,
                'timestamp': msg.timestamp.isoformat()
            } for msg in messages
        ][::-1]  # Đảo ngược để có thứ tự gần nhất đến xa nhất
    
    def update_chat_history(self, sender, content):
        """Cập nhật lịch sử chat JSON với tin nhắn mới"""
        if not isinstance(self.chat_history, list):
            self.chat_history = []
            
        self.chat_history.append({
            'sender': sender,
            'content': content,
            'timestamp': str(datetime.now())
        })
        
        # Giới hạn lịch sử lưu trữ
        if len(self.chat_history) > 50:
            self.chat_history = self.chat_history[-50:]
            
        self.save()

class ChatMessage(models.Model):
    SENDER_CHOICES = (
        ('user', 'User'),
        ('bot', 'Bot'),
    )
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.sender}: {self.content[:50]}"
