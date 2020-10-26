from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.edit import FormMixin
from django.contrib.auth.models import User

from django.views.generic import DetailView, ListView

from .forms import ComposeForm
from .models import Thread, ChatMessage


class InboxView(LoginRequiredMixin, ListView):
    # currently a generic view
    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)


class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
    # view in charge of the chat threads
    template_name = 'chat/thread.html'
    form_class = ComposeForm
    success_url = './'

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        # responsible for retriving the thread or 404 it
        other_username  = self.kwargs.get("username")
        obj, created    = Thread.objects.get_or_new(self.request.user, other_username)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        # handling the post of a message rejects if not authorized
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        thread = self.get_object()
        user = self.request.user
        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(user=user, thread=thread, message=message)
        return super().form_valid(form)

# searches for the user specified and takes the searcher to that chat room
def search_list_view(request, *args, **kwargs):
    template_name = 'chat/search.html'
    form_class = ComposeForm
    search_id = request.POST.get('search_user')
    context = {}
    if search_id != None:
        new_url = f'http://127.0.0.1:8000/chat/{search_id}'
        return redirect(new_url)
    
    return render(request, template_name, context)

# lists all chats the user is in 
def thread_list_view(request, *args, **kwargs):
    template_name = 'chat/inbox.html'
    queryset = Thread.objects.by_user(request.user)
    context = {"object_list": queryset}
    return render(request, template_name, context)