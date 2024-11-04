from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from datetime import timedelta

from apps.cms.models import Visit

class VisitorTrackingMiddleware(MiddlewareMixin):
    # Список разрешенных путей для учета посещений
    TRACKED_PATHS = ['/', '/about/', '/contact/', '/faq/', '/services/', '/services_details/']
    TIME_LIMIT = timedelta(hours=1)  # Время ограничения для повторных посещений

    def process_request(self, request):
        # Игнорируем запросы к admin и static
        if request.path.startswith('/admin') or request.path.startswith('/static'):
            return

        # Учитываем посещения только для путей из TRACKED_PATHS
        if request.path not in self.TRACKED_PATHS:
            return

        # Получаем IP-адрес
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        # Получаем User-Agent и URL
        user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
        url_path = request.path

        # Проверяем, заходил ли пользователь в последний час
        one_hour_ago = timezone.now() - self.TIME_LIMIT
        recent_visit = Visit.objects.filter(
            ip_address=ip_address,
            user_agent=user_agent,
            url_path=url_path,
            timestamp__gte=one_hour_ago  # Условие для времени посещения
        ).exists()

        # Если запись о посещении в последний час не найдена, создаем новую
        if not recent_visit:
            Visit.objects.create(ip_address=ip_address, user_agent=user_agent, url_path=url_path)