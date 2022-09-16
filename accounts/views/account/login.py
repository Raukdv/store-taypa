from django.contrib.auth.views import LoginView, LogoutView


class LoginView(LoginView):
    template_name = 'panel/account/login.html'

class LogoutView(LogoutView):
    template_name = 'panel/account/logged_out.html'
