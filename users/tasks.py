from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email(email):
    from django.core.mail import send_mail
    from django.conf import settings

    print("🔥 TASK STARTED:", email)

    try:
        result = send_mail(
            subject="Welcome 🎉",
            message="Thanks for registering!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        print("📧 EMAIL RESULT:", result)

    except Exception as e:
        print("❌ EMAIL ERROR:", str(e))