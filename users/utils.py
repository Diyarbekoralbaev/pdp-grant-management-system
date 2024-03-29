from django.core.mail import send_mail
from random import randint

def send_otp(otp, email):
    try:
        subject = 'OTP for password reset'
        message = f'Your OTP is {otp}'
        from_email = 'diyarbekdev@gmail.com'
        recipient_list = [email]
        print(f"{subject}\n{message}\n{from_email}\n{recipient_list}")
        return send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        print(e)
        return False


def generate_otp():
    return randint(100000, 999999)
