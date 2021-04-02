from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *
from .forms import *


from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls_site/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls_site/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls_site/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if (request.user.is_authenticated):
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            return render(request, 'polls_site/detail.html', { # send back the voting form
                'question': question,
                'error_message': "You didn't select anything.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            # if success -> HttpResponseRedirect, so it prevents data from being sent(posted) twice. Like when user pressed BACK button twice
            return HttpResponseRedirect(reverse('polls_site:results', args=(question.id,))) 
    else:
        return HttpResponseRedirect(reverse('polls_site:results', args=(question.id,)))


#-------------------------------------------------------------------------------------------------------
def log_out(request):
    logout(request)
    redirect_url = request.GET.get('next') or reverse('index')
    return redirect(redirect_url)

def log_in(request):
    if request.method == 'POST':
        logout(request)
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(request.GET['next'])
            else:
                form.add_error('Invalid credentials!')
    else:  # GET
        form = LoginForm()
    return render(request, 'polls_site/login.html', {'form': form})


def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            logout(request)
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_again = form.cleaned_data['password_again']
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'User already exists!')
            elif password != password_again:
                form.add_error('password_again', 'Password mismatch!')
            else:
                user = User.objects.create_user(username, email, password)
                login(request, user)
                return render(request, 'polls_site/index.html')
    else:  # GET
        form = RegistrationForm()
    return render(request, 'polls_site/signup.html', {'form': form})

