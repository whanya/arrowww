from django.contrib import admin
from .models import ContactRequest, MailingSettings
from django import forms

@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'contact', 'message', 'created_at')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'contact', 'message')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

    @admin.display(description='Сообщение')
    def short_message(self, obj):
        return (obj.message[:50] + '...') if len(obj.message) > 50 else obj.message

class MailingSettingsForm(forms.ModelForm):
    class Meta:
        model = MailingSettings
        fields = '__all__'
        widgets = {
            'email_password': forms.PasswordInput(render_value=True),
        }

@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    form = MailingSettingsForm
    list_display = ("email_enabled", "telegram_enabled", "db_save_enabled")
    fieldsets = (
        ("Общие настройки", {
            "fields": ("email_enabled", "telegram_enabled", "db_save_enabled"),
        }),
        ("Настройки почты", {
            "fields": (
                "email_from", 
                "email_password",
                "email_host",
                "email_port",
                "email_use_ssl",
                "email_subject",
                "email_recipients"
            ),
        }),
        ("Настройки Telegram", {
            "fields": ("telegram_bot_token", "telegram_chat_ids"),
        }),
        
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['email_password'].widget = forms.PasswordInput(render_value=True)
        return form