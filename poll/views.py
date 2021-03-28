from django.shortcuts import render, redirect, HttpResponse
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate

from .forms import CreatePollForm
from .models import Poll


def home(request):
    polls = Poll.objects.all()

    context = {
        'polls': polls
    }
    return render(request, 'poll/home.html', context)

#To create new poll
def create(request):
    #If user is not logged in
    if request.user.is_anonymous:
        return render(request, 'poll/login.html')

    if request.method == 'POST':
        form = CreatePollForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('home')
    else:
        form = CreatePollForm()

    context = {'form': form}
    return render(request, 'poll/create.html', context)


def results(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    context = {
        'poll': poll
    }
    return render(request, 'poll/results.html', context)


def vote(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    if request.method == 'POST':

        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.option_one_count += 1
        elif selected_option == 'option2':
            poll.option_two_count += 1
        elif selected_option == 'option3':
            poll.option_three_count += 1
        else:
            return HttpResponse(400, 'Invalid form option')

        poll.save()

        return redirect('results', poll.id)

    context = {
        'poll': poll
    }
    return render(request, 'poll/vote.html', context)


def loginuser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            #return render(request, "poll/home.html")
            return redirect("/")
        else:
            return render(request, 'poll/login.html')
    return render(request, 'poll/login.html')


def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password1 = request.POST['password1']

        user = User.objects.create_user(
            first_name=first_name, email=email, username=username, password=password)
        user.save()
        messages.success(
            request, 'Your Account has  been created. Please Login')
        return render(request, 'poll/login.html')
    else:
        return render(request, 'poll/signup.html')


def logoutuser(request):
    logout(request)
    #return render(request, "poll/home.html")
    return redirect("/")
