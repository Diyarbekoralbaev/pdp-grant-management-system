from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.signals import user_logged_out
from django.contrib.auth.signals import user_login_failed
from .models import UserModel


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    user.last_logged_device = request.META.get('HTTP_USER_AGENT')
    user.last_logged_ip = request.META.get('REMOTE_ADDR')
    user.save()


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    user.last_logged_device = None
    user.last_logged_ip = None
    user.save()


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, request, **kwargs):
    user = UserModel.objects.get(username=credentials.get('username'))
    user.last_logged_device = request.META.get('HTTP_USER_AGENT')
    user.last_logged_ip = request.META.get('REMOTE_ADDR')
    user.save()
