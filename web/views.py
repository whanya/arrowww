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
    # SEO метатеги для главной страницы
    seo_context = {
        'meta_title': 'ARROWWW — Профессиональная веб-разработка и digital-решения',
        'meta_description': 'Создаем современные сайты и digital-продукты для бизнеса. От проектирования до запуска и продвижения. Обсудим ваш проект?',
        'meta_keywords': 'веб-разработка, создание сайтов, digital-агентство, заказать сайт, продвижение сайтов',
        'meta_robots': 'index, follow',
        'meta_author': 'ARROWWW',
        'og_title': 'ARROWWW — Веб-разработка и digital-решения',
        'og_description': 'Создаём сайты и digital-продукты для роста вашего бизнеса. Оставьте заявку!',
        'og_url': 'https://arrowww.ru',
        'og_image': 'https://arrowww.ru/static/images/og-preview.jpg',
    }
    
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
            return redirect('success')
    else:
        form = ContactRequestForm()

    # Объединяем SEO контекст с формой
    context = {**seo_context, 'form': form}
    return render(request, 'web/index.html', context)


def success(request):
    seo_context = {
        'meta_title': 'Заявка отправлена — ARROWWW',
        'meta_description': 'Ваша заявка успешно отправлена! Мы свяжемся с вами в ближайшее время для обсуждения проекта.',
        'meta_robots': 'noindex, follow',
        'og_title': 'Заявка отправлена — ARROWWW',
        'og_description': 'Спасибо за вашу заявку! Мы скоро свяжемся с вами.',
        'og_url': 'https://arrowww.ru/success',
    }
    return render(request, 'web/success.html', seo_context)


def privacy(request):
    seo_context = {
        'meta_title': 'Политика конфиденциальности — ARROWWW',
        'meta_description': 'Политика конфиденциальности данных на сайте ARROWWW. Как мы обрабатываем и защищаем вашу информацию.',
        'meta_robots': 'noindex, follow',
        'og_title': 'Политика конфиденциальности — ARROWWW',
        'og_description': 'Узнайте о нашей политике обработки персональных данных.',
        'og_url': 'https://arrowww.ru/privacy',
    }
    return render(request, 'web/privacy.html', seo_context)


def case0(request):
    seo_context = {
        'meta_title': 'Кейс: Разработка корпоративного сайта — ARROWWW',
        'meta_description': 'Пример успешного проекта по созданию корпоративного сайта. Подробное описание процесса разработки и результатов.',
        'meta_keywords': 'кейс, портфолио, корпоративный сайт, пример работы',
        'meta_robots': 'index, follow',
        'og_title': 'Кейс: Корпоративный сайт — ARROWWW',
        'og_description': 'Посмотрите наш кейс по разработке корпоративного сайта',
        'og_url': 'https://arrowww.ru/case0',
    }
    return render(request, 'web/case0.html', seo_context)


def case1(request):
    seo_context = {
        'meta_title': 'Кейс: Интернет-магазин — ARROWWW',
        'meta_description': 'Разработка интернет-магазина под ключ. Особенности реализации, используемые технологии и достигнутые результаты.',
        'meta_keywords': 'кейс, интернет-магазин, e-commerce, пример работы',
        'meta_robots': 'index, follow',
        'og_title': 'Кейс: Интернет-магазин — ARROWWW',
        'og_description': 'Пример разработки интернет-магазина с нуля',
        'og_url': 'https://arrowww.ru/case1',
    }
    return render(request, 'web/case1.html', seo_context)


def case2(request):
    seo_context = {
        'meta_title': 'Кейс: Лендинг пейдж — ARROWWW',
        'meta_description': 'Создание эффективного лендинга для увеличения конверсии. Дизайн, разработка и результаты проекта.',
        'meta_keywords': 'кейс, лендинг, landing page, одностраничник',
        'meta_robots': 'index, follow',
        'og_title': 'Кейс: Лендинг пейдж — ARROWWW',
        'og_description': 'Пример создания конверсионного лендинга',
        'og_url': 'https://arrowww.ru/case2',
    }
    return render(request, 'web/case2.html', seo_context)


def sitemap(request):
    # Для sitemap.xml не нужны HTML метатеги
    return render(request, 'web/sitemap.xml', content_type='application/xml')


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
