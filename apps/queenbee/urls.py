from django.urls import path 

from apps.queenbee.moduls.index import crm_index
from apps.queenbee.moduls.kanban import crm_kanban_index, crm_kanban_detail, crm_add_list, crm_add_board, crm_edit_board, crm_delete_board

urlpatterns = [
    path('', crm_index, name="crm_index"),
    path('kanban/', crm_kanban_index, name="crm_kanban_index"),
    path('kanban/<int:id>/', crm_kanban_detail, name="crm_kanban_detail"),
    path('kanban/create/<int:board_id>/', crm_add_list, name="crm_add_list"),
    path('kanban/board/', crm_add_board, name="crm_add_board"),
    path('kanban/delete_board/<int:board_id>/', crm_delete_board, name='crm_delete_board'),
    path('kanban/edit_board/<int:board_id>/', crm_edit_board, name='crm_edit_board'),
]