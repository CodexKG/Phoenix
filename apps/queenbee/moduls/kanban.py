from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import logging

from apps.kanban import models, forms

logger = logging.getLogger(__name__)

def crm_kanban_index(request):
    boards = models.Board.objects.all().order_by('-created_at')
    return render(request, 'queenbee/kanban/index.html', locals())

def crm_kanban_detail(request, id):
    board = get_object_or_404(models.Board, id=id)
    lists = models.List.objects.filter(board=board).prefetch_related('card_lists')  # Prefetch карточки для каждого списка
    return render(request, 'queenbee/kanban/detail.html', {'board': board, 'lists': lists})

def crm_add_list(request, board_id):
    if request.method == 'POST':
        board = get_object_or_404(models.Board, id=board_id)
        form = forms.ListForm(request.POST)
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.user = request.user
            new_list.board = board

            # Получаем последнюю позицию
            last_position = models.List.objects.filter(board=board).count() + 1

            new_list.position = last_position
            new_list.save()
            return JsonResponse({
                'title': new_list.title,
                'position': new_list.position,
                'list_id': new_list.id
            })
    return JsonResponse({'error': 'Ошибка создания списка'}, status=400)