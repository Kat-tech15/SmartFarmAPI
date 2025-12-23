from django.core.mail import send_mail
from . models import EmailOTP
from django.conf import settings
from twilio.rest import Client


def send_sms_otp(phone_number, otp_code):
    accoount_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
    auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
    from_number = getattr(settings, 'TWILIO_PHONE_NUMBER', None)

    if not accoount_sid or not auth_token or not from_number:
        print("Twilio credentials missing; skipping SMS Send.")
        return None
    
    client = Client(accoount_sid, auth_token)
    message =  f"Your OTP code is {otp_code}. It expires in 5 minutes."

    try:
        response = client.messages.create(
            body=message, 
            from_=from_number,
            to=phone_number
        )
        print("OTP sent via Twilio:", response.sid)
        return response
    except Exception as e:
        print("Twilio SMS sending error:", e)
        return None


    
def send_otp_to_user(user, code=None, via_sms=False):
    if code is None:
        otp_obj = EmailOTP.create_for_user(user)
    else:
        expire_at = EmailOTP.expiry_time()
        otp_obj = EmailOTP.objects.create(user=user, code=code, expire_at=expire_at)

    if via_sms:
        phone = getattr(user, 'phone', None)
        if not phone:
            print("User has no phone number; cannot send SMS OTP.")
        else:
            send_sms_otp(phone, otp_obj.code)
        return otp_obj
    
    from_email = getattr(settings, 'EMAIL_HOST_USER', settings.DEFAULT_FROM_EMAIL)
    send_mail(
        "Your OTP Code ✔",
        f"Your verification code is {otp_obj.code}",
        from_email,
        [user.email],
        fail_silently=False,
    )
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