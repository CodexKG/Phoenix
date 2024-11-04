from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.admin.utils import label_for_field
from django.contrib import admin
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from django.utils.timezone import make_aware
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from django.db import transaction
import uuid, json, logging, traceback, asyncio

from apps.crm.models import Billing
from apps.crm.forms import BillingForm
from apps.queenbee.permissions import permission_required

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
        email = request.POST.get('email')
        fullname = request.POST.get('fullname', '').strip()
        phone = request.POST.get('phone')
        delivery_from = request.POST.get('from_city')
        delivery_to = request.POST.get('to_city')
        type_product = request.POST.get('appearance')
        
        # Парсим fullname и разделяем его на first_name и last_name
        name_parts = fullname.split()
        if len(name_parts) == 1:
            first_name = name_parts[0]
            last_name = ''  # Оставляем пустым, если фамилия не указана
        elif len(name_parts) == 2:
            first_name, last_name = name_parts
        else:
            first_name = name_parts[0]
            last_name = ' '.join(name_parts[1:])  # Объединяем все оставшиеся части в last_name

        # Преобразуем числовые данные с заменой запятых на точки
        try:
            weight = float(request.POST.get('weight', '0').replace(',', '.'))
            length = float(request.POST.get('length', '0').replace(',', '.'))
            width = float(request.POST.get('width', '0').replace(',', '.'))
            height = float(request.POST.get('height', '0').replace(',', '.'))
            volume_product = length * width * height
            delivery_price = float(request.POST.get('delivery_price', '0').replace(',', '.'))
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Некорректные числовые данные. Убедитесь, что все числовые значения введены правильно.'})

        # Собираем данные для создания записи в модели Billing
        billing_data = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "delivery_from": delivery_from,
            "delivery_to": delivery_to,
            "type_product": type_product,
            "weight_product": weight,
            "length_product": length,
            "width_product": width,
            "height_product": height,
            "volume_product": volume_product,
            "delivery_price": delivery_price,
            "total_price": delivery_price,
            "billing_status": Billing.BillingStatusChoices.ISSUED
        }

        # Проверка наличия обязательных полей
        if not all([email, first_name, phone, delivery_from, delivery_to, type_product]):
            return JsonResponse({'success': False, 'error': 'Все обязательные поля должны быть заполнены.'})

        # Создаем запись в модели Billing
        billing = Billing(**billing_data)
        billing.save()

        return JsonResponse({'success': True, 'message': 'Заявка успешно создана'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
def parse_custom_date_string(date_str, end_of_day=False):
    date_format = '%b %d'
    current_year = datetime.now().year
    naive_date = datetime.strptime(f"{date_str} {current_year}", f"{date_format} %Y")
    
    if end_of_day:
        naive_date = naive_date.replace(hour=23, minute=59, second=59)
    else:
        naive_date = naive_date.replace(hour=0, minute=0, second=0)

    aware_date = make_aware(naive_date)
    
    return aware_date

def parse_short_date(date_str):
    try:
        return datetime.strptime(date_str + ' ' + str(datetime.now().year), '%b %d %Y').date()
    except ValueError as e:
        print(f"Failed to parse date string {date_str}: {e}")
        return None

@staff_member_required(login_url='/admin/login/')
@permission_required('crm_index_lead', 'Просмотр раздела лидогенерация')
def crm_index_billings(request):
    today = datetime.today().date()
    end_date = today
    start_date = today - timedelta(days=7)

    date_input = request.GET.get('CRMDateRange')
    if date_input:
        start_str, end_str = date_input.split(' to ')

        start_date = parse_custom_date_string(start_str)
        end_date = parse_custom_date_string(end_str, end_of_day=True)

    default_start_date = start_date.strftime('%b %d')
    default_end_date = end_date.strftime('%b %d')

    return render(request, 'queenbee/billing/index.html', locals())


@staff_member_required(login_url='/admin/login/')
@permission_required('crm_detail_billings', 'Просмотр биллингов')
def crm_detail_billings(request, id):
    billing = get_object_or_404(Billing, id=id)
    # products = Product.objects.all()

    if request.method == "POST":
        form = BillingForm(request.POST, request.FILES, instance=billing, request=request)
        # formset = BillingProductFormSet(request.POST, instance=billing)
        # image_formset = BillingImageFormSet(request.POST, request.FILES, instance=billing)

        if 'save_detail' in request.POST:
            if form.is_valid():
                try:
                    with transaction.atomic():
                        updated_billing = form.save()
                        # image_formset.save()
                    messages.success(request, 'Биллинг успешно обновлен')
                    return redirect('crm_report_index' if updated_billing.billing_type != 'Лидогенерация' else 'crm_index_billings')
                except Exception as e:
                    messages.error(request, f'Ошибка при сохранении биллинга: {str(e)}')
            else:
                messages.error(request, 'Форма содержит ошибки')
            return render(request, 'crm/billing/detail.html', {
                'form': form,
                # 'formset': formset,
                # 'image_formset': image_formset,
                # 'products': products,
                'billing': billing,
            })

        # if 'save' in request.POST:
        #     if form.is_valid() and formset.is_valid() and image_formset.is_valid():
        #         try:
        #             with transaction.atomic():
        #                 billing = form.save()
        #                 formset.instance = billing
        #                 formset.save()
        #                 image_formset.instance = billing
        #                 image_formset.save()
        #             messages.success(request, 'Биллинг успешно сохранен!')
        #             response_url = reverse('crm_report_index' if billing.billing_type != 'Лидогенерация' else 'crm_index_billings')
        #             return JsonResponse({'url': response_url, 'message': 'Биллинг успешно сохранен!'})
        #         except Exception as e:
        #             messages.error(request, f'Ошибка при создании биллинга: {str(e)}')
        #     else:
        #         messages.error(request, 'Форма содержит ошибки')
        #     return JsonResponse({'form_errors': form.errors.as_json(), 'formset_errors': formset.errors, 'image_formset_errors': image_formset.errors}, status=400)
    else:
        form = BillingForm(instance=billing, request=request)
        # formset = BillingProductFormSet(instance=billing)
        # image_formset = BillingImageFormSet(instance=billing)

    return render(request, 'queenbee/billing/detail.html', {
        'form': form,
        # 'formset': formset,
        # 'image_formset': image_formset,
        # 'products': products,
        'billing': billing,
    })


@staff_member_required(login_url='/admin/login/')
@permission_required('crm_detail_billings', 'Добавление биллингов')
def crm_add_billings(request):
    # products = Product.objects.all()
    if request.method == "POST":
        form = BillingForm(request.POST, request.FILES, request=request)
        # formset = BillingProductFormSet(request.POST, instance=form.instance)
        # image_formset = BillingImageFormSet(request.POST, request.FILES, instance=form.instance)

        if form.is_valid():
            try:
                with transaction.atomic():
                    billing = form.save(commit=False)
                    billing.save()
                    
                    form.instance = billing
                    form.save_m2m()

                    # formset.instance = billing
                    # formset.save()

                    # image_formset.instance = billing
                    # image_formset.save()
                    
                    # if billing.billing_payment_status == 'Оплачен':
                    #     cash = billing.cash
                    #     if cash:
                    #         original_amount = cash.total_amount
                    #         cash.total_amount += billing.client_gave_money
                    #         cash.save()
                    #         CashHistory.objects.create(
                    #             cash=cash,
                    #             title=f'Оплата биллинга {billing.id}',
                    #             amount=billing.client_gave_money,
                    #             transaction_type='Доход'
                    #         )
                            # logger.info(f"Updated cash total amount from {original_amount} to {cash.total_amount}")

                    # Отправка уведомления в Telegram-группу, если Вид получения товара - Доставка
                    # if billing.billing_receipt_type == 'Доставка':
                    #     billing_products = billing.billing_products.all()  # Получаем продукты
                    #     asyncio.run(send_post_billing(
                    #         id=billing.id,
                    #         products="\n".join([f"{item.product} ({item.quantity} шт)" for item in billing_products]),
                    #         city=billing.city,
                    #         street=billing.street,
                    #         phone=billing.phone,
                    #         delivery_price=billing.delivery_price,
                    #         total_price=billing.total_price,
                    #         billing_receipt_type=billing.billing_receipt_type,
                    #         first_name=billing.first_name,
                    #         last_name=billing.last_name,
                    #         payment_code=billing.payment_code
                    #     ))

                messages.success(request, 'Биллинг успешно создан!')
                return redirect('crm_detail_billings', id=billing.id)
            except Exception as e:
                # logger.error(f"Ошибка при создании биллинга: {e}")
                messages.error(request, f'Ошибка при создании биллинга: {e}')
                if billing and billing.id:
                    billing.delete()
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
            # if not form.is_valid():
            #     logger.error(f"Form errors: {form.errors}")
            # if not formset.is_valid():
            #     logger.error(f"Formset errors: {formset.errors}")
            # if not image_formset.is_valid():
            #     logger.error(f"Image formset errors: {image_formset.errors}")
    else:
        form = BillingForm(request=request)
        # formset = BillingProductFormSet()
        # image_formset = BillingImageFormSet()

    return render(request, 'queenbee/billing/add.html', {
        'form': form,
        # 'formset': formset,
        # 'image_formset': image_formset,
        # 'products': products
    })


@staff_member_required(login_url='/admin/login/')
@permission_required('crm_detail_billings', 'Обновление биллингов')
def crm_update_billings(request, id):
    billing = get_object_or_404(Billing, id=id)
    if request.method == "POST":
        form = BillingForm(request.POST, instance=billing)
        # formset = BillingProductFormSet(request.POST, instance=billing)
        if form.is_valid():
            try:
                with transaction.atomic():
                    billing = form.save()
                    # formset.save()
                messages.success(request, 'Биллинг успешно обновлен!')
                return redirect('crm_detail_billings', id=billing.id)
            except Exception as e:
                messages.error(request, f'Ошибка при обновлении биллинга: {str(e)}')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = BillingForm(instance=billing)
        # formset = BillingProductFormSet(instance=billing)

    return render(request, 'queenbee/billing/update.html', {
        'form': form,
        # 'formset': formset,
        'billing': billing,
    })

@staff_member_required(login_url='/admin/login/')
def get_billing_data(request):
    fields = request.GET.get('fields')
    list_display = fields.split(',') if fields else ['id', 'billing_source', 'total_price', 'phone', 'delivery_price', 'billing_receipt_type', 'payment_code', 'billing_status', 'billing_payment_status', 'billing_payment', 'created']

    # Получаем значения начальной и конечной дат из GET-запроса
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    # Преобразуем строки в объекты date
    start_date = parse_short_date(start_date_str) if start_date_str else (datetime.today() - timedelta(days=7)).date()
    end_date = parse_short_date(end_date_str) if end_date_str else datetime.today().date()

    # Преобразуем конечную дату в конец дня
    end_date = datetime.combine(end_date, datetime.max.time())

    billing_receipt_type = request.GET.get('billing_receipt_type')
    billing_status = request.GET.get('billing_status')
    billing_payment_status = request.GET.get('billing_payment_status')
    billing_payment = request.GET.get('billing_payment')

    try:
        # Формируем фильтры, включая диапазон дат
        filters = {
            'created__range': (make_aware(datetime.combine(start_date, datetime.min.time())), make_aware(datetime.combine(end_date, datetime.max.time()))),
            'billing_type': Billing.BillingTypeChoices.LEADGENERATION
        }

        # Если пользователь курьер, показываем только биллинги со статусом "Оформлен"
        
        if billing_receipt_type:
            filters['billing_receipt_type'] = billing_receipt_type
        if billing_payment_status:
            filters['billing_payment_status'] = billing_payment_status
        if billing_payment:
            filters['billing_payment'] = billing_payment

        # Применяем фильтры и сортируем по дате создания
        billings = Billing.objects.filter(**filters).order_by('-created')
        billings_list = list(billings.values(*list_display))

        model_admin = admin.site._registry[Billing]
        field_names = {
            field: label_for_field(field, Billing, model_admin)
            for field in list_display
        }

        return JsonResponse({
            'billings': billings_list,
            'field_names': field_names,
        })

    except Exception as e:
        print("Error", e)
        return JsonResponse({'error': str(e)}, status=500)