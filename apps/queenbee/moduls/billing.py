from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import uuid

from apps.crm.models import Billing

@require_POST
def calculate_delivery(request):
    try:
        # Получаем данные из запроса и проверяем их наличие
        weight = request.POST.get('weight')
        length = request.POST.get('length')
        width = request.POST.get('width')
        height = request.POST.get('height')

        # Проверка наличия всех значений
        if not all([weight, length, width, height]):
            return JsonResponse({'success': False, 'error': 'Все параметры должны быть заполнены.'})

        # Преобразование значений в float
        weight = float(weight)
        length = float(length)
        width = float(width)
        height = float(height)

        # Рассчитываем объем и стоимость доставки
        volume_product = length * width * height
        if volume_product > 0:
            delivery_price = (weight / volume_product) * 0.35
        else:
            delivery_price = 0

        # Возвращаем рассчитанную стоимость доставки
        return JsonResponse({
            'success': True,
            'delivery_price': round(delivery_price, 2)  # Округляем до двух знаков
        })
    except ValueError:
        return JsonResponse({'success': False, 'error': 'Неверные данные. Проверьте, что все поля заполнены числовыми значениями.'})

@require_POST
def create_billing(request):
    try:
        # Получаем данные из формы для создания заявки
        billing_data = {
            "email": request.POST.get('email'),
            # "first_name": request.POST.get('first_name'),
            # "last_name": request.POST.get('last_name'),
            # "fullname": request.POST.get('fullname'),
            "phone": request.POST.get('phone'),
            "delivery_from": request.POST.get('from_city'),
            "delivery_to": request.POST.get('to_city'),
            "type_product": request.POST.get('appearance'),
            "weight_product": float(request.POST.get('weight')),
            "length_product": float(request.POST.get('length')),
            "width_product": float(request.POST.get('width')),
            "height_product": float(request.POST.get('height')),
            "volume_product": float(request.POST.get('length')) * float(request.POST.get('width')) * float(request.POST.get('height')),  # Вычисляем объем
            "delivery_price": float(request.POST.get('delivery_price')),
            "billing_status": Billing.BillingStatusChoices.ISSUED
        }

        # Проверка наличия обязательных полей
        if not all(billing_data.values()):
            return JsonResponse({'success': False, 'error': 'Все поля должны быть заполнены.'})

        # Создаем запись в модели Billing
        billing = Billing(**billing_data)
        billing.save()

        return JsonResponse({'success': True, 'message': 'Заявка успешно создана'})
    except ValueError:
        return JsonResponse({'success': False, 'error': 'Неверные данные. Проверьте, что все числовые поля заполнены корректными значениями.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
