from decouple import config

def chat_links(request):
    id_chat = config('CHAT_ID')
    return dict(id_chat=id_chat)