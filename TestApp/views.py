from django.shortcuts import render

from django.views import View
from .forms import *


def home(request):
    return render(request, 'empty.html', {'title': 'empty'})


class AddUser(View):
    def get(self, request):
        return render(request, 'empty.html', {'form': UserForm, 'title': 'add user'})

    def post(self, request):
        form = UserForm(request.POST)
        context = {'title': 'add user'}
        if form.is_valid():
            form.save()
        else:
            context.update({'form': form})
        return render(request, 'empty.html', context)


class AssignFriends(View):
    def get(self, request):
        return render(request, 'empty.html', {'form': FriendForm, 'title': 'add friend'})

    def post(self, request):
        form = FriendForm(request.POST)
        context = {'title': 'add friend'}
        if form.is_valid():
            username_a = form.cleaned_data.get('username_a')
            username_b = form.cleaned_data.get('username_b')
            user_a = User.objects.get(username=username_a)
            user_b = User.objects.get(username=username_b)
            user_a.friends.add(user_b)
        else:
            context.update({'form': form})
        return render(request, 'empty.html', context)
