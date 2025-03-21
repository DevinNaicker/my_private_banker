"""
URL configuration for my_private_banker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from my_app.views.auth_views import signup, CustomLoginView, CustomLogoutView
from my_app.views.budget_views import user_budget, add_budget
from my_app.views.transaction_views import user_transactions, add_transaction
from my_app.views import homepage

urlpatterns = [
    path("", homepage, name="homepage"),
    path("signup/", signup, name="signup"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("budget/", user_budget, name="user_budget"),
    path("budget/add/", add_budget, name="add_budget"),
    path("transactions/", user_transactions, name="user_transactions"),
    path("transactions/add/", add_transaction, name="add_transaction"),
    path('admin/', admin.site.urls),
]
