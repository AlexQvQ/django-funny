from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Joke
from django.contrib import messages
from .forms import JokeForm
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

def index(request):
    return render(request, 'main/index.html')

@require_POST
def vote_joke(request, joke_id):
    joke = get_object_or_404(Joke, pk=joke_id)
    cookie_name = f'joke_{joke_id}_voted'
    
    if request.COOKIES.get(cookie_name):
        messages.warning(request, 'Вы уже голосовали за эту шутку! Проголосуйте через месяц, так как автору было лень регистрацию делать, и сейчас хранится все в куки, следующими коммитами добавит :D')
        return redirect('jokes')
    
    joke.votes += 1
    joke.save()
    
    response = redirect('jokes')
    response.set_cookie(cookie_name, 'true', max_age=30*24*60*60)
    messages.success(request, 'Ваш голос учтен! Спасибо!')
    return response

def jokes(request):

    error = ""
    if request.method == 'POST':
        form = JokeForm(request.POST)
        if form.is_valid():
            joke = form.save(commit=False)
            joke.votes = 0
            joke.save()
            return redirect('jokes')
        else:
            error = "Ошибка отправки"
    jokes = Joke.objects.all()
    form = JokeForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'main/Jokes.html', {'jokes' : jokes, 'context' : context})

