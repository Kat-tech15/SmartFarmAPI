from django.core.mail import send_mail
from . models import EmailOTP
import os

def send_otp_to_user(user):
    otp = EmailOTP.generate_code()
    expire_at = EmailOTP.expiry_time()

    EmailOTP.objects.create(
        user=user,
        code=otp,
        expire_at=expire_at,
    )

    send_mail(
        "Your OTP Code ✔",
        f"Your verification code is {otp}",
        os.getenv('EMAIL_HOST_USER'),
        [user.email],
        fail_silently=False,
    )