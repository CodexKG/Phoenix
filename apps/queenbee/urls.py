from django.urls import path 

from apps.queenbee.moduls.index import crm_index
from apps.queenbee.moduls import kanban

urlpatterns = [
    path('', crm_index, name="crm_index"),
    path('kanban/', kanban.crm_kanban_index, name="crm_kanban_index"),
    path('kanban/<int:id>/', kanban.crm_kanban_detail, name="crm_kanban_detail"),
    path('kanban/create/<int:board_id>/', kanban.crm_add_list, name="crm_add_list"),
    path('kanban/board/', kanban.crm_add_board, name="crm_add_board"),
    path('kanban/delete_board/<int:board_id>/', kanban.crm_delete_board, name='crm_delete_board'),
    path('kanban/edit_board/<int:board_id>/', kanban.crm_edit_board, name='crm_edit_board'),
    path('kanban/list/<int:list_id>/add_card/', kanban.crm_add_card, name='crm_add_card'),
]