from django.core.mail import send_mail
from . models import EmailOTP
from django.conf import settings
import africastalking
import os


def send_sms_otp(phone_number, otp_code):
    username = os.getenv('AT_USERNAME') or getattr(settings, 'AT_USERNAME', None)
    api_key = os.getenv('AT_API_KEY') or getattr(settings, 'AT_API_KEY', None)

    if not username or not api_key:
        print("Africa's Talking credentials missing; skipping SMS send.")
        return None
    
    africastalking.initialize(username, api_key)
    sms = africastalking.SMS
    message = f"Your OTP code is {otp_code}. It expires in 5 minutes."

    try:
        response = sms.send(message, [phone_number])
        return response
    except Exception as e:
        print("SMS sending error:", e)
        return None
    
def send_otp_to_user(user, code=None, send_via_sms=True):
    if code is None:
        otp_obj = EmailOTP.create_for_user(user)
    else:
        expire_at = EmailOTP.expiry_time()
        otp_obj = EmailOTP.objects.create(user=user, code=code, expire_at=expire_at)

    
    from_email = os.getenv('EMAIL_HOST_USER') or settings.DEFAULT_FROM_EMAIL
    send_mail(
        "Your OTP Code ✔",
        f"Your verification code is {otp_obj.code}",
        from_email,
        [user.email],
        fail_silently=False,
    )

    if send_via_sms and getattr(user, 'phone', None):
        send_sms_otp(user.phone, otp_obj.code)

    return otp_obj

def notify_admin_contact(message_instance):
    subject = f"New contact Message: {message_instance.subject if hasattr(message_instance, 'subject') else ''}"
    body = (
        f"Name: {message_instance.name}\n"
        f"Email: {message_instance.email}\n\n"
        f"Message:\n{message_instance.message}\n\n"
        f"Submitted at: {message_instance.created_at}"
    )
    admin_email = settings.EMAIL_HOST_USER or settings.DEFAULT_FROM_EMAIL
    try:
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [admin_email],
            fail_silently=False,
        )
    except Exception as e:
        print("notify_admin_contact email erroe:", e)