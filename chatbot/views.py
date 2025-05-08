from django.http import JsonResponse
from django.shortcuts import render
import requests
import json
import uuid
from django.conf import settings
from datetime import datetime
from accounts.models import Account
from .models import ChatSession, ChatMessage
from langdetect import detect, LangDetectException
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def account_infor(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return JsonResponse({'username': 'none'})
        account = Account.objects.filter(id=request.user.id).first()
        return JsonResponse({'username': account.full_name, 'date_joined': account.date_joined}, status=200)


def check_auth(request):
    """Check if the user is authenticated and return status"""
    if request.method == 'GET':
        return JsonResponse({
            'is_authenticated': request.user.is_authenticated,
            'username': request.user.full_name if request.user.is_authenticated else None
        })


def update_session(request):
    """Update a chat session with user information when an anonymous user logs in"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            chat_id = data.get('chat_id')
            
            if chat_id and request.user.is_authenticated:
                try:
                    session = ChatSession.objects.get(id=chat_id)
                    session.user = request.user
                    session.save()
                    return JsonResponse({'success': True})
                except ChatSession.DoesNotExist:
                    return JsonResponse({'error': 'Chat session not found'}, status=404)
            
            return JsonResponse({'error': 'Invalid request'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def chat_view(request):
    context = {
        'current_time': datetime.now()
    }
    return render(request, 'chat.html', context)


def get_or_create_session(request, session_id=None):
    if session_id:
        try:
            session = ChatSession.objects.get(id=session_id)
            if request.user.is_authenticated and session.user is None:
                session.user = request.user
                session.save()
            return session
        except ChatSession.DoesNotExist:
            pass
    
    session = ChatSession.objects.create(
        user=request.user if request.user.is_authenticated else None
    )
    return session


def detect_language(text):
    try:
        lang = detect(text)
        if lang == 'vi':
            return 'vi'
        else:
            return 'en' 
    except LangDetectException:
        return 'en'
    

def generate_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query', '')
            chat_id = data.get('chat_id')
            
            lang = detect_language(query)
            
            session = get_or_create_session(request, chat_id)
            
            ChatMessage.objects.create(
                session=session,
                sender='user',
                content=query
            )
            
            session.update_chat_history('user', query)
            
            recent_messages = session.get_recent_messages(5)
            
            chat_history = []
            for msg in recent_messages:
                role = "user" if msg['sender'] == 'user' else "model"
                chat_history.append({
                    'role': role,
                    'parts': [{'text': msg['content']}]
                })
            
            response = requests.post(
                f"{settings.API_CHAT}/generate",
                json={
                    'query': query,
                    'history_chat': chat_history, 
                    'lang': lang,
                    'chat_id': str(session.id)
                },
                headers={'Content-Type': 'application/json'},
                timeout=60
            )
            
            if response.status_code == 200:
                response_data = response.json()
                bot_response = response_data.get('response', '')
                
                ChatMessage.objects.create(
                    session=session,
                    sender='bot',
                    content=bot_response
                )
                
                session.update_chat_history('bot', bot_response)
                
                return JsonResponse({
                    'response': bot_response,
                    'chat_id': str(session.id)
                })
            else:
                error_message = "Sorry, an error occurred while processing your request."
                if lang == 'vi':
                    error_message = f"Xin lỗi, có lỗi xảy ra khi xử lý yêu cầu của bạn. (Mã lỗi: {response.status_code})"
                
                ChatMessage.objects.create(
                    session=session,
                    sender='bot',
                    content=error_message
                )
                
                session.update_chat_history('bot', error_message)
                
                return JsonResponse({
                    'response': error_message,
                    'chat_id': str(session.id)
                }, status=500)
                
        except requests.RequestException as e:
            session = get_or_create_session(request, data.get('chat_id'))
            lang = data.get('lang', 'en')
            error_message = "Sorry, could not connect to the chat service. Please try again later."
            if lang == 'vi':
                error_message = "Xin lỗi, không thể kết nối đến dịch vụ chat. Vui lòng thử lại sau."
            
            ChatMessage.objects.create(
                session=session,
                sender='bot',
                content=error_message
            )
            
            session.update_chat_history('bot', error_message)
            
            return JsonResponse({
                'response': error_message,
                'chat_id': str(session.id)
            }, status=503)
        except json.JSONDecodeError:
            session = get_or_create_session(request)
            error_message = "Sorry, invalid request data."
            
            ChatMessage.objects.create(
                session=session,
                sender='bot',
                content=error_message
            )
            
            session.update_chat_history('bot', error_message)
            
            return JsonResponse({
                'response': error_message,
                'chat_id': str(session.id)
            }, status=400)
        except Exception as e:
            session = get_or_create_session(request, data.get('chat_id'))
            error_message = f"An unexpected error occurred: {str(e)}"
            
            ChatMessage.objects.create(
                session=session,
                sender='bot',
                content=error_message
            )
            
            session.update_chat_history('bot', error_message)
            
            return JsonResponse({
                'response': error_message,
                'chat_id': str(session.id)
            }, status=500)
    
    session = get_or_create_session(request)
    return JsonResponse({
        'response': "Invalid request. Please use POST method.",
        'chat_id': str(session.id)
    }, status=405)


def get_initial_message(request):
    if request.method == 'GET':
        is_authenticated = request.user.is_authenticated
        
        session = get_or_create_session(request)
        
        if is_authenticated:
            username = request.user.full_name or request.user.username
            message = f"Hello {username}! I'm EKKA, your shopping assistant. How can I help you today?"
        else:
            message = "Hello! I'm EKKA, your shopping assistant. How can I help you today?"
        
        ChatMessage.objects.create(
            session=session,
            sender='bot',
            content=message
        )
        
        session.update_chat_history('bot', message)
        
        return JsonResponse({
            'message': message,
            'chat_id': str(session.id)
        })


def new_chat_session(request):
    session = get_or_create_session(request)
    
    if request.user.is_authenticated:
        username = request.user.full_name or request.user.username
        message = f"Hello {username}! I'm EKKA, your shopping assistant. How can I help you today?"
    else:
        message = "Hello! I'm EKKA, your shopping assistant. How can I help you today?"
    
    ChatMessage.objects.create(
        session=session,
        sender='bot',
        content=message
    )
    
    session.update_chat_history('bot', message)
    
    return JsonResponse({
        'message': message,
        'chat_id': str(session.id)
    })


def get_chat_history(request, session_id):
    try:
        session = ChatSession.objects.get(id=session_id)
        
        if request.user.is_authenticated and session.user is None:
            session.user = request.user
            session.save()
        
        messages = []
        for msg in session.messages.all():
            messages.append({
                'content': msg.content,
                'sender': msg.sender,
                'timestamp': msg.timestamp.isoformat()
            })
        
        return JsonResponse({
            'chat_id': str(session.id),
            'messages': messages,
            'is_authenticated': request.user.is_authenticated,
            'username': request.user.full_name if request.user.is_authenticated else None
        })
    except ChatSession.DoesNotExist:
        return JsonResponse({
            'error': 'Chat session not found'
        }, status=404)
