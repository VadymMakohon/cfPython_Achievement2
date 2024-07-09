# Django authentication libraries
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


def login_view(request):
    error_message = None
    form = AuthenticationForm()
    # when user hits "login", then POST request is generated
    if request.method == "POST":
        # read the data sent by the form via POST request
        form = AuthenticationForm(data=request.POST)
        # if form has requisite data
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            # validate user
            user = authenticate(username=username, password=password)
            # if user is authenticated, then use pre-defined Django function to login
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                # send user to desired page
                return redirect("recipes:recipes_list")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    context = {"form": form, "error_message": "ooops... something is not right"}
    return render(request, "auth/login.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, "You've successfully logged out.")
    return redirect("success")