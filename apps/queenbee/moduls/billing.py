from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import uuid

from apps.crm.models import Billing

@require_POST
def calculate_delivery(request):
    try:
        # Получаем данные из запроса
        weight = float(request.POST.get('weight', 0))
        length = float(request.POST.get('length', 0))
        width = float(request.POST.get('width', 0))
        height = float(request.POST.get('height', 0))

        # Рассчитываем объем и стоимость доставки
        volume_product = length * width * height
        delivery_price = (weight / volume_product) * 0.35 if volume_product > 0 else 0

        # Возвращаем рассчитанную стоимость доставки
        return JsonResponse({
            'success': True,
            'delivery_price': round(delivery_price, 2)  # Округляем до двух знаков
        })
    except ValueError:
        return JsonResponse({'success': False, 'error': 'Неверные данные'})

@require_POST
def create_billing(request):
    try:
        # Получаем данные из формы для создания заявки
        billing_data = {
            "email": request.POST.get('email'),
            "first_name": request.POST.get('first_name'),
            "last_name": request.POST.get('last_name'),
            "phone": request.POST.get('phone'),
            "delivery_from": request.POST.get('from_city'),
            "delivery_to": request.POST.get('to_city'),
            "type_product": request.POST.get('appearance'),
            "weight_product": float(request.POST.get('weight')),
            "length_product": float(request.POST.get('length')),
            "width_product": float(request.POST.get('width')),
            "height_product": float(request.POST.get('height')),
            "volume_product": float(request.POST.get('volume_product')),
            "delivery_price": float(request.POST.get('delivery_price')),
            "billing_status": Billing.BillingStatusChoices.ISSUED
        }

        # Создаем запись в модели Billing
        billing = Billing(**billing_data)
        billing.save()

        return JsonResponse({'success': True, 'message': 'Заявка успешно создана'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
