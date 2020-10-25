from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm

# Form for creation of a new user
def RegisterView(reponse):
    if reponse.method == "POST":
        form = RegisterForm(reponse.POST)
        if form.is_valid():
            form.save()
        return redirect("/home")
    else:
        form = RegisterForm()

    context = {"form": form}
    return render(reponse, 'account/register.html', context)