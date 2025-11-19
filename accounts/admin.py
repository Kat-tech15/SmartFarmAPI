from django.contrib import admin
from .models import ContactMessage, CustomUser, EmailOTP

admin.site.register(ContactMessage)
admin.site.register(CustomUser)
admin.site.register(EmailOTP)