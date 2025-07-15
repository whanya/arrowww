from django.db import models

class ContactRequest(models.Model):
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.contact})"

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

class MailingSettings(models.Model):
    #Общие настройки
    email_enabled = models.BooleanField("Отправка на почту", default=True)
    telegram_enabled = models.BooleanField("Отправка в телеграм", default=True)
    whatsapp_enabled = models.BooleanField("Отправка в вацап", default=True)
    db_save_enabled = models.BooleanField("Сохранение в БД", default=True)

    #Настройки почты
    email_from = models.EmailField("Email отправителя", blank=True, null=True)
    email_password = models.CharField("Пароль отправителя", max_length=255, blank=True, null=True)
    email_host = models.CharField("SMTP сервер", max_length=255, default='smtp.yandex.ru')
    email_port = models.IntegerField("SMTP порт", default=465)
    email_use_ssl = models.BooleanField("Использовать SSL", default=True)
    email_subject = models.CharField("Тема письма", max_length=255, blank=True, null=True)
    email_recipients = models.TextField(
        "Получатели (через запятую)", 
        default='studenikin000@yandex.ru',
        help_text="Пример: email1@example.com, email2@example.com"
    )

    #Настройки телеграмма
    telegram_bot_token = models.CharField("Токен бота", max_length=255, blank=True, null=True)
    telegram_chat_ids = models.TextField(
        "ID чатов (через запятую)",
        help_text="Пример: 123456789, 987654321",
        blank=True,
        null=True
    )


    #Получаем email
    def get_email_recipients_list(self):
        if not self.email_recipients:
            return []
        return [email.strip() for email in self.email_recipients.split(",") if email.strip()]

    #Получаем айди чата тг
    def get_telegram_chat_ids_list(self):
        if not self.telegram_chat_ids:
            return []
        return [int(chat_id.strip()) for chat_id in self.telegram_chat_ids.split(",")]
    
    def __str__(self):
        return "Настройки рассылки"
    
    class Meta:
        verbose_name = 'Настройка рассылки'
        verbose_name_plural = "Настройки рассылки"