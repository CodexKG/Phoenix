from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import logging
import json

from apps.kanban import models, forms
from apps.queenbee.permissions import permission_required
from apps.erp.models import Employee

logger = logging.getLogger(__name__)


@staff_member_required(login_url='/admin/login')
@permission_required('crm_kanban_index', 'Просмотр раздела Задачник')
def crm_kanban_index(request):
    boards = models.Board.objects.all().order_by('-created_at')
    form = forms.BoardForm()

    return render(request, 'queenbee/kanban/index.html', {
        'boards': boards,
        'form': form
    })


@staff_member_required(login_url='/admin/login/')
@permission_required('crm_kanban_detail', 'Детальный просмотр раздела Задачник')
def crm_kanban_detail(request, id):
    board = get_object_or_404(models.Board, id=id)
    lists = models.List.objects.filter(
        board=board).prefetch_related('card_lists')
    employees = Employee.objects.all()

    # Формы для добавления карточки и вложений
    card_form = forms.CardForm()
    attachment_formset = forms.AttachmentInlineFormset()

    return render(request, 'queenbee/kanban/detail.html', {
        'board': board,
        'lists': lists,
        'employees': employees,
        'card_form': card_form,
        'attachment_formset': attachment_formset,
    })


def crm_add_list(request, board_id):
    # Логируем начало запроса
    logger.info("Получен запрос на добавление списка")

    if request.method == 'POST':
        logger.info("Метод запроса POST, пытаемся получить доску")
        board = get_object_or_404(models.Board, id=board_id)

        logger.info("Доска найдена: %s", board.title)
        form = forms.ListForm(request.POST)

        if form.is_valid():
            logger.info("Форма валидна, продолжаем создание списка")
            new_list = form.save(commit=False)
            new_list.user = request.user
            new_list.board = board

            # Получаем последнюю позицию
            last_position = models.List.objects.filter(board=board).count() + 1
            new_list.position = last_position

            logger.info("Присвоена позиция: %d", last_position)
            new_list.save()

            logger.info("Список успешно сохранен с ID: %d", new_list.id)
            return JsonResponse({
                'title': new_list.title,
                'position': new_list.position,
                'list_id': new_list.id,
                'success': True
            })
        else:
            logger.error("Ошибка в форме: %s", form.errors)

    logger.error("Ошибка создания списка")
    return JsonResponse({'error': 'Ошибка создания списка'}, status=400)


@staff_member_required(login_url='/admin/login/')
def crm_add_board(request):
    # Логируем начало запроса
    logger.info("Получен запрос на добавление новой доски")

    if request.method == 'POST':
        form = forms.BoardForm(request.POST)
        if form.is_valid():
            logger.info("Форма валидна, продолжаем создание доски")
            new_board = form.save(commit=False)
            new_board.owner = request.user
            new_board.save()

            logger.info("Доска успешно сохранена с ID: %d", new_board.id)
            return JsonResponse({
                'title': new_board.title,
                'board_id': new_board.id
            })

        else:
            logger.error("Ошибка в форме: %s", form.errors)
            return JsonResponse({'error': 'Ошибка создания доски'}, status=400)

    logger.error("Метод запроса не POST")
    return JsonResponse({'error': 'Метод запроса не POST'}, status=400)


def crm_delete_board(request, board_id):
    if request.method == 'POST':
        try:
            board = models.Board.objects.get(id=board_id)
            board.delete()
            return JsonResponse({'success': True})
        except models.Board.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Доска не найдена'})
    return JsonResponse({'success': False, 'error': 'Неверный запрос'})


def crm_edit_board(request, board_id):
    if request.method == 'POST':
        try:
            board = models.Board.objects.get(id=board_id)
            data = json.loads(request.body)
            new_title = data.get('title')
            if new_title:
                board.title = new_title
                board.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Название не может быть пустым'})
        except models.Board.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Доска не найдена'})
    return JsonResponse({'success': False, 'error': 'Неверный запрос'})

# Карточки
# Представление для создания карточки


def crm_add_card(request, list_id):
    list_obj = get_object_or_404(models.List, id=list_id)

    if request.method == 'POST':
        form = forms.CardForm(request.POST, request.FILES)
        formset = forms.AttachmentInlineFormset(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            # Создаем карточку
            card = form.save(commit=False)
            card.user = request.user
            card.list = list_obj
            card.position = list_obj.card_lists.count() + 1
            card.save()
            form.save_m2m()

            # Сохраняем все вложения из formset и добавляем текущего пользователя к каждому из них
            formset.instance = card
            attachments = formset.save(commit=False)
            for attachment in attachments:
                attachment.user = request.user
                attachment.save()
            formset.save()

            return JsonResponse({'success': True, 'card_title': card.title, 'card_description': card.description, 'card_id': card.id})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    else:
        form = forms.CardForm()
        formset = forms.AttachmentInlineFormset()

    return render(request, 'kanban/card_form.html', {
        'form': form,
        'formset': formset,
    })


@csrf_exempt
def crm_update_card_positions(request):
    if request.method == "POST":
        data = json.loads(request.body)
        card_ids = data.get('cardIds', [])
        new_list_id = data.get('listId', None)

        if not new_list_id:
            return JsonResponse({'success': False, 'error': 'New list ID is required'})

        try:
            new_list = models.List.objects.get(id=new_list_id)
        except models.List.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'List not found'})

        # Обновляем позиции и список для каждой карточки
        for index, card_id in enumerate(card_ids):
            try:
                card = models.Card.objects.get(id=card_id)
                card.position = index  # Новая позиция
                card.list = new_list  # Обновляем список
                card.save()
            except models.Card.DoesNotExist:
                return JsonResponse({'success': False, 'error': f'Card with ID {card_id} not found'})

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required(login_url='/admin/login/')
def crm_delete_card(request, card_id):
    try:
        card = models.Card.objects.get(id=card_id)
        card.delete()
        return JsonResponse({'success': True})
    except models.Card.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Карточка не найдена'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
def crm_update_card_positions(request):
    if request.method == "POST":
        data = json.loads(request.body)
        card_ids = data.get('cardIds', [])
        new_list_id = data.get('listId', None)

        if not new_list_id:
            return JsonResponse({'success': False, 'error': 'New list ID is required'})

        try:
            new_list = models.List.objects.get(id=new_list_id)
        except models.List.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'List not found'})

        # Обновляем карточки в новом порядке
        for index, card_id in enumerate(card_ids):
            try:
                if card_id is None:
                    continue  # Игнорируем пустые значения
                card = models.Card.objects.get(id=card_id)
                card.position = index
                card.list = new_list
                card.save()
            except models.Card.DoesNotExist:
                logger.error(f'Карточка с ID {card_id} не найдена')
                continue

        # Создаем словарь с количеством задач для каждого списка
        task_counts = {}
        for kanban_list in models.List.objects.filter(board=new_list.board):
            task_counts[kanban_list.id] = kanban_list.card_lists.count()

        return JsonResponse({'success': True, 'taskCounts': task_counts})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})
