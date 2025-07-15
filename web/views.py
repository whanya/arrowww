from django.shortcuts import render, redirect
from .forms import ContactRequestForm
from .services import send_email_via_smtp, send_to_telegram
import logging
from .models import MailingSettings
from django.db import transaction
from threading import Thread
from django.conf import settings

logger = logging.getLogger(__name__)


def index(request):
    if request.method == 'POST':
        form = ContactRequestForm(request.POST)
        if form.is_valid():
            form.save()
            mailing_settings = MailingSettings.objects.first()
            data = form.cleaned_data
            
            # Сохранение в БД в отдельной транзакции
            if not mailing_settings or mailing_settings.db_save_enabled:
                try:
                    with transaction.atomic():
                        form.save()
                except Exception as e:
                    logger.error(f"Ошибка сохранения в БД: {e}")

            # Запуск отправки уведомлений в фоновом режиме
            if settings.DEBUG:
                # В режиме разработки выполняем синхронно для удобства отладки
                send_notifications(mailing_settings, data)
            else:
                # В продакшене - асинхронно
                Thread(target=send_notifications, args=(mailing_settings, data)).start()
            return redirect('success')  # потом сюда сделаем страницу-спасибо
    else:
        form = ContactRequestForm()

    return render(request, 'web/index.html', {'form': form})

def success(request):
    return render(request, 'web/success.html')


def send_notifications(mailing_settings, data):
    """Функция для отправки всех уведомлений"""
    # Отправка email
    if mailing_settings and mailing_settings.email_enabled:
        try:
            send_email_via_smtp(mailing_settings, data)
        except Exception as e:
            logger.error(f"Ошибка отправки email: {e}")

    # Отправка в Telegram
    if not mailing_settings or mailing_settings.telegram_enabled:
        try:
            send_to_telegram(data)
        except Exception as e:
            logger.error(f"Ошибка отправки в Telegram: {e}")