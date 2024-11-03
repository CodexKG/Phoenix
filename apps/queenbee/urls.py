from django.urls import path 

from apps.queenbee.moduls.index import crm_index
from apps.queenbee.moduls import kanban
from apps.queenbee.moduls import users
from apps.queenbee.moduls import employees
from apps.queenbee.moduls import billing

urlpatterns = [
    path('', crm_index, name="crm_index"),

    #kanban
    path('kanban/', kanban.crm_kanban_index, name="crm_kanban_index"),
    path('kanban/<int:id>/', kanban.crm_kanban_detail, name="crm_kanban_detail"),
    path('kanban/create/<int:board_id>/', kanban.crm_add_list, name="crm_add_list"),
    path('kanban/board/', kanban.crm_add_board, name="crm_add_board"),
    path('kanban/delete_board/<int:board_id>/', kanban.crm_delete_board, name='crm_delete_board'),
    path('kanban/edit_board/<int:board_id>/', kanban.crm_edit_board, name='crm_edit_board'),
    path('kanban/list/<int:list_id>/add_card/', kanban.crm_add_card, name='crm_add_card'),
    path('kanban/update_card_positions/', kanban.crm_update_card_positions, name='update_card_positions'),
    path('kanban/card/<int:card_id>/delete/', kanban.crm_delete_card, name='crm_delete_card'),

    #users
    path('login/', users.crm_login, name="crm_login"),

    #employee
    path('employee/', employees.crm_employee_index, name="crm_employee_index"),
    path('employee/add/', employees.crm_employee_detail, name="crm_employee_add"),
    path('employee/<int:id>/', employees.crm_employee_detail, name="crm_employee_detail"),
    path('get_employee_data/', employees.get_report_employee_data, name='get_report_employee_data'),
    path('upload_employee_data/', employees.upload_employee_data, name="upload_employee_data"),
    path('export_employees_to_excel/', employees.export_employees_to_excel, name='export_employees_to_excel'),

    #billing
    path('calculate_delivery/', billing.calculate_delivery, name='calculate_delivery'),
    path('create_billing/', billing.create_billing, name='create_billing'),
]