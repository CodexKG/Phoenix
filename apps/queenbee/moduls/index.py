from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from datetime import timedelta

from apps.crm.models import Billing
from apps.cms.models import Visit
from apps.queenbee.permissions import permission_required

@staff_member_required(login_url='/admin/login')
@permission_required('crm_index', 'Просмотр главного раздела')
def crm_index(request):
    # Определяем период (например, последние 14 дней)
    last_two_weeks = timezone.now() - timedelta(days=14)
    
    # Получаем общее количество посещений за последние 14 дней
    total_visits_last_two_weeks = Visit.objects.filter(timestamp__gte=last_two_weeks).count()

    # Список страниц, которые будем анализировать
    tracked_paths = ['/', '/about/', '/contact/', '/faq/', '/services/', '/services_details/']

    # Создаем словарь для хранения процента посещений каждой страницы
    pages_percentage = {}

    if total_visits_last_two_weeks > 0:
        # Для каждой страницы считаем количество посещений и рассчитываем процент
        for path in tracked_paths:
            page_visits_count = Visit.objects.filter(timestamp__gte=last_two_weeks, url_path=path).count()
            page_percentage = (page_visits_count / total_visits_last_two_weeks) * 100
            pages_percentage[path] = round(page_percentage, 2)
    else:
        # Если посещений за последние 14 дней нет, устанавливаем процент в 0 для всех страниц
        for path in tracked_paths:
            pages_percentage[path] = 0.0

    # Получаем последние 7 дней биллингов и группируем их по дню недели
    last_seven_days = timezone.now() - timedelta(days=7)
    billings = Billing.objects.filter(created__gte=last_seven_days)

    # Группируем данные по дням недели
    billing_stats = {
        'Sunday': 0,
        'Monday': 0,
        'Tuesday': 0,
        'Wednesday': 0,
        'Thursday': 0,
        'Friday': 0,
        'Saturday': 0
    }

    for billing in billings:
        weekday = billing.created.strftime('%A')
        billing_stats[weekday] += 1

    # Передаем значения в шаблон
    return render(request, 'queenbee/index.html', {
        'pages_percentage': pages_percentage,
        'billings': billings,
        'billing_stats': billing_stats,  # Передаем статистику по биллингам
        'new_billings_count': billings.count()
    })