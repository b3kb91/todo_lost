from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import RegistrationView, UsersView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('project/<int:pk>/users/', UsersView.as_view(), name='users_check'),

]
