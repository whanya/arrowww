from django.contrib import admin
from .models import ContactRequest

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

# Register your models here.
