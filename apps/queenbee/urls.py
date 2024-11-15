from django.urls import path

from apps.queenbee.moduls.index import crm_index
from apps.queenbee.moduls import kanban, users, employees, billing, group_permissions, visit, partners

urlpatterns = [
    path('', crm_index, name="crm_index"),

    # kanban
    path('kanban/', kanban.crm_kanban_index, name="crm_kanban_index"),
    path('kanban/<int:id>/', kanban.crm_kanban_detail, name="crm_kanban_detail"),
    path('kanban/card/<int:card_id>/attachments/',
         kanban.get_card_attachments, name='get_card_attachments'),
    path('kanban/create/<int:board_id>/',
         kanban.crm_add_list, name="crm_add_list"),
    path('kanban/board/', kanban.crm_add_board, name="crm_add_board"),
    path('kanban/delete_board/<int:board_id>/',
         kanban.crm_delete_board, name='crm_delete_board'),
    path('kanban/edit_board/<int:board_id>/',
         kanban.crm_edit_board, name='crm_edit_board'),
    path('kanban/list/<int:list_id>/add_card/',
         kanban.crm_add_card, name='crm_add_card'),
    path('kanban/update_card_positions/',
         kanban.crm_update_card_positions, name='update_card_positions'),
    path('kanban/card/<int:card_id>/delete/',
         kanban.crm_delete_card, name='crm_delete_card'),

    # users
    path('login/', users.crm_login, name="crm_login"),
    path('user/', users.crm_index_users, name='crm_index_user'),
    path('user/add/', users.crm_detail_users, name='crm_add_user'),
    path('user/<int:id>/', users.crm_detail_users, name="crm_detail_user"),
    path('get_user_data/', users.get_user_data, name='get_user_data'),
    path('profile/user/<int:id>', users.crm_user_profile, name="crm_user_profile"),
    path('change-password/', users.change_password, name='change_password'),
    path('profile/setting/<int:id>/',
         users.crm_user_setting, name="crm_user_setting"),

    # employee
    path('employee/', employees.crm_employee_index, name="crm_employee_index"),
    path('employee/add/', employees.crm_employee_detail, name="crm_employee_add"),
    path('employee/<int:id>/', employees.crm_employee_detail,
         name="crm_employee_detail"),
    path('get_employee_data/', employees.get_report_employee_data,
         name='get_report_employee_data'),
    path('upload_employee_data/', employees.upload_employee_data,
         name="upload_employee_data"),
    path('export_employees_to_excel/', employees.export_employees_to_excel,
         name='export_employees_to_excel'),

    # billing
    path('billing/', billing.crm_index_billings, name='crm_index_billings'),
    path('billing/detail/<int:id>/', billing.crm_detail_billings,
         name='crm_detail_billings'),
    path('billing/add/', billing.crm_add_billings, name='crm_add_billings'),
    path('get_billing_data/', billing.get_billing_data, name='get_billing_data'),
    path('calculate_delivery/', billing.calculate_delivery,
         name='calculate_delivery'),
    path('create_billing/', billing.create_billing, name='create_billing'),

    # groups
    path('group/', group_permissions.crm_group_index, name="crm_group_index"),
    path('group/add/', group_permissions.crm_group_detail, name="crm_group_add"),
    path('group/<int:id>/', group_permissions.crm_group_detail,
         name="crm_group_detail"),
    path('get_group_data/', group_permissions.get_group_data, name='get_group_data'),

    # visit
    path('visit/', visit.visit_statistics, name="visit_statistics"),

    # partners
    path('partner/', partners.crm_partner_index, name="crm_partner_index"),
    path('partner/add/', partners.crm_partner_detail, name="crm_partner_add"),
    path('partner/<int:id>/', partners.crm_partner_detail,
         name="crm_partner_detail"),
    path('get_partner_data/', partners.get_partner_data, name='get_partner_data'),
]
