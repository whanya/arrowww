from django.core.mail import send_mail, get_connection
from django.conf import settings
import requests
import logging
from .models import MailingSettings


logger = logging.getLogger(__name__)
def send_to_telegram(data):
    mailing_settings = MailingSettings.objects.first()
    if not mailing_settings or not mailing_settings.telegram_enabled:
        return None

    bot_token = mailing_settings.telegram_bot_token
    chat_ids = mailing_settings.get_telegram_chat_ids_list()
    
    if not bot_token or not chat_ids:
        return None

    message = f"Новая заявка!\nИмя: {data['name']}\nКонтакт: {data['contact']}\nСообщение: {data['message']}"
    
    responses = []
    for chat_id in chat_ids:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        params = {'chat_id': chat_id, 'text': message}
        try:
            response = requests.post(url, params=params)
            responses.append(response.json())
        except Exception as e:
            logger.error(f"Ошибка отправки в Telegram (chat_id {chat_id}): {e}")
    
    return responses

def send_email_via_smtp(mailing_settings, form_data):
    """Отправка email с использованием настроек SMTP"""
    if not all([
        mailing_settings.email_from,
        mailing_settings.email_password,
        mailing_settings.email_host,
        mailing_settings.email_port is not None
    ]):
        logger.error("Не все SMTP настройки заполнены")
        return False

    subject = mailing_settings.email_subject or 'Новая форма отправлена'
    message = f'''
    Имя: {form_data['name']}
    Контакт: {form_data['contact']}
    Сообщение: {form_data['message']}
    '''
    recipients = mailing_settings.get_email_recipients_list()
    
    if not recipients:
        logger.error("Не указаны получатели email")
        return False

    try:
        connection = get_connection(
            host=mailing_settings.email_host,
            port=mailing_settings.email_port,
            username=mailing_settings.email_from,
            password=mailing_settings.email_password,
            use_ssl=mailing_settings.email_use_ssl
        )
        
        send_mail(
            subject,
            message,
            mailing_settings.email_from,
            recipients,
            connection=connection
        )
        return True
    except Exception as e:
        logger.error(f"Ошибка отправки email: {e}")
        return False
    

