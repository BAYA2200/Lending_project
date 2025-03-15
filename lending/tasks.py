from celery import shared_task
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

@shared_task
def send_email_task(recipient_email, subject, message):
    """Отправка email с обработкой ошибок"""
    try:
        # Проверяем корректность email
        validate_email(recipient_email)

        send_mail(
            subject=subject,
            message=message,
            from_email="aydarov2101@gmail.com",
            recipient_list=[recipient_email],
            fail_silently=False,
        )
        return {"status": "success", "message": "Email отправлен"}

    except ValidationError:
        return {"status": "error", "message": "Некорректный email"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
