from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from .models import Thread, ChatMessage
from django.template.loader import render_to_string

@login_required
def messages_page(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    context = {
        'Threads': threads
    }
    return render(request, 'messages.html', context)

@login_required
def fetch_messages(request):
    # Retrieve messages associated with the current user
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    # Render the messages HTML template with the fetched messages
    html_content = render_to_string('messages_content.html', {'Threads': threads})
    return JsonResponse({'html_content': html_content})

@login_required
@require_POST
def send_message(request):
    if request.method == 'POST':
        message_text = request.POST.get('message')
        # Save the message to the database
        thread_id = request.POST.get('thread_id')  # Assuming you have a hidden input field in your HTML form to pass the thread ID
        thread = Thread.objects.get(id=thread_id)
        ChatMessage.objects.create(thread=thread, user=request.user, message=message_text)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
