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

# Create your models here.
