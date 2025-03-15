from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import AdminSettings
from .tasks import send_email_task  # Импортируем Celery-задачу

@api_view(["POST"])
def send_application(request):
    """Принимает заявку и отправляет данные менеджеру на email (асинхронно через Celery)"""
    data = request.data
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")

    if not name or not email or not phone:
        return Response({"error": "Все поля (name, email, phone) обязательны"}, status=400)

    # Проверяем корректность email пользователя
    try:
        validate_email(email)
    except ValidationError:
        return Response({"error": "Некорректный email"}, status=400)

    # Получаем email менеджера из базы
    settings = AdminSettings.objects.first()
    if not settings:
        return Response({"error": "Email менеджера не настроен в админке"}, status=500)

    manager_email = settings.manager_email

    # Запускаем задачу Celery
    task = send_email_task.delay(
        recipient_email=manager_email,
        subject="Новая заявка",
        message=f"Имя: {name}\nEmail: {email}\nТелефон: {phone}"
    )

    return Response({"task_id": task.id, "status": "Заявка отправлена"}, status=200)
