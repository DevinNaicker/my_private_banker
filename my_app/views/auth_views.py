from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect

# Signup View
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # Redirect to login after signup
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})

# Login View (using Django's built-in LoginView)
class CustomLoginView(auth_views.LoginView):
    template_name = "login.html"

# Logout View (using Django's built-in LogoutView)
class CustomLogoutView(auth_views.LogoutView):
    pass  # Uses Django's default behavior