from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import logging

from apps.kanban import models, forms

logger = logging.getLogger(__name__)

@login_required
def crm_kanban_index(request):
    boards = models.Board.objects.all().order_by('-created_at')
    form = forms.BoardForm()
    
    return render(request, 'queenbee/kanban/index.html', {
        'boards': boards,
        'form': form
    })

def crm_kanban_detail(request, id):
    board = get_object_or_404(models.Board, id=id)
    lists = models.List.objects.filter(board=board).prefetch_related('card_lists')  # Prefetch карточки для каждого списка
    return render(request, 'queenbee/kanban/detail.html', {'board': board, 'lists': lists})

def crm_add_list(request, board_id):
    logger.info("Получен запрос на добавление списка")  # Логируем начало запроса
    
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
                'list_id': new_list.id
            })
        else:
            logger.error("Ошибка в форме: %s", form.errors)
    
    logger.error("Ошибка создания списка")
    return JsonResponse({'error': 'Ошибка создания списка'}, status=400)

@login_required
def crm_add_board(request):
    logger.info("Получен запрос на добавление новой доски")  # Логируем начало запроса
    
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