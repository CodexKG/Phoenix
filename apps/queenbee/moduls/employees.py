from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.utils import label_for_field
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib import admin
import traceback, logging, json

from apps.erp.models import Employee
from apps.erp.forms import EmployeeForm

@login_required(login_url='/admin/login/')
def crm_employee_index(request):
    return render(request, 'queenbee/employee/index.html')

@login_required(login_url='/admin/login/')
def crm_employee_detail(request, id=None):
    employee = get_object_or_404(Employee, id=id) if id else None

    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if "update" in request.POST and form.is_valid():
            # log_change.delay(request.user.id, f"Обновлены данные сотрудника {form.cleaned_data.get('first_name')} {form.cleaned_data.get('last_name')} пользователем {request.user.username} {request.user.first_name} {request.user.last_name}")
            form.save()
            return redirect('crm_employee_detail', id=employee.id)
        elif "delete" in request.POST:
            # log_change.delay(request.user.id, f"Удалены данные сотрудника {employee.first_name} {employee.last_name} пользователем {request.user.username} {request.user.first_name} {request.user.last_name}")
            employee.delete()
            return redirect('crm_employee_index')
        else:
            if form.is_valid():
                form.save()
                # log_change.delay(request.user.id, f"Добавлены данные сотрудника {form.cleaned_data.get('first_name')} {form.cleaned_data.get('last_name')} пользователем {request.user.username} {request.user.first_name} {request.user.last_name}")
                return redirect('crm_employee_index')
    else:
        form = EmployeeForm(instance=employee)

    context = {
        'form': form,
        'employee': employee
    }
    return render(request, 'crm/employee/detail.html', context)

def get_report_employee_data(request):
    fields = request.GET.get('fields')
    list_display = fields.split(',') if fields else ['id', 'first_name', 'last_name', 'employee_position', 'phone', 'created']

    city_id = request.GET.get('city')
    employee_position = request.GET.get('employee_position')

    try:
        filters = {}
        if city_id:
            filters['city__id'] = city_id
        if employee_position:
            filters['employee_position'] = employee_position

        employees = Employee.objects.filter(**filters).values_list(*list_display, named=True).order_by('-created')

        model_admin = admin.site._registry[Employee]
        field_names = {
            field: label_for_field(field, Employee, model_admin)
            for field in list_display
        }

        return JsonResponse({
            'employees': [employee._asdict() for employee in employees],
            'field_names': field_names,
        })

    except Exception as e:
        print("Error", e)
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)
    
def upload_employee_data(request):
    # if request.method == 'POST' and request.FILES:
    #     excel_file = request.FILES['employee_file']
    #     df = pd.read_excel(excel_file, header=None)
    #     df.columns = ['Unnamed: 0', 'Город', 'Аккаунт пользователя', 'Имя', 'Фамилия', 'Номер телефона', 'Электронная почта', 'Адрес', 'Дата рождения', 'Должность', 'Комментарии']  # Явное переименование столбцов
    #     df['Дата рождения'] = pd.to_datetime(df['Дата рождения'], errors='coerce')

    #     print("Columns in the dataframe:", df.columns)
    #     print("Data sample:", df.head())

    #     df = df.iloc[1:]
    #     df = df.where(pd.notnull(df), None)

    #     for index, row in df.iterrows():
    #         email_or_username = row['Электронная почта']
    #         if email_or_username:
    #             try:
    #                 user = User.objects.create(
    #                     username=email_or_username, 
    #                     email=email_or_username
    #                 )
    #                 user.set_password(email_or_username)
    #                 user.save()
    #             except Exception as error:
    #                 print("Error", error)
    #                 user = User.objects.create(
    #                     username=f"{email_or_username}{random.randint(1, 100)}", 
    #                     email=f"{email_or_username}{random.randint(1, 100)}"
    #                 )
    #                 user.set_password(email_or_username)
    #                 user.save()
    #         else:
    #             user = None

    #         city_title = row['Город']
    #         city, _ = City.objects.get_or_create(title=city_title)

    #         date_of_birth = row['Дата рождения'] if not pd.isnull(row['Дата рождения']) else None

    #         employee = Employee.objects.create(
    #             user=user,
    #             first_name=row['Имя'],
    #             last_name=row['Фамилия'],
    #             phone=row['Номер телефона'],
    #             email=email_or_username,
    #             address=row['Адрес'],
    #             date_of_birth=date_of_birth,
    #             employee_position=row['Должность']
    #         )
    #         employee.city.set([city])

    #     return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)

# @staff_member_required(login_url='/admin/login/')
def export_employees_to_excel(request):
    # workbook = Workbook()
    # sheet = workbook.active
    # sheet.title = 'Employees'

    # headers = [
    #     'ID', 'Имя', 'Фамилия', 'Номер телефона', 'Электронная почта',
    #     'Адрес', 'Дата рождения', 'Должность', 'Комментарии', 'Дата создания',
    #     'Город', 'Аккаунт пользователя'
    # ]
    
    # for col_num, header in enumerate(headers, 1):
    #     cell = sheet.cell(row=1, column=col_num)
    #     cell.value = header
    #     cell.font = Font(bold=True)

    # for row_num, employee in enumerate(Employee.objects.all(), 2):
    #     sheet.cell(row=row_num, column=1, value=employee.id)
    #     sheet.cell(row=row_num, column=2, value=employee.first_name)
    #     sheet.cell(row=row_num, column=3, value=employee.last_name)
    #     sheet.cell(row=row_num, column=4, value=employee.phone)
    #     sheet.cell(row=row_num, column=5, value=employee.email)
    #     sheet.cell(row=row_num, column=6, value=employee.address)
    #     sheet.cell(row=row_num, column=7, value=employee.date_of_birth.strftime('%Y-%m-%d') if employee.date_of_birth else '')
    #     sheet.cell(row=row_num, column=8, value=employee.get_employee_position_display())
    #     sheet.cell(row=row_num, column=9, value=employee.note)
    #     sheet.cell(row=row_num, column=10, value=employee.created.strftime('%Y-%m-%d %H:%M:%S'))
    #     sheet.cell(row=row_num, column=11, value=', '.join([city.title for city in employee.city.all()]))
    #     sheet.cell(row=row_num, column=12, value=str(employee.user))

    # for column in sheet.columns:
    #     max_length = 0
    #     column = list(column)
    #     for cell in column:
    #         try:
    #             if len(str(cell.value)) > max_length:
    #                 max_length = len(cell.value)
    #         except:
    #             pass
    #     adjusted_width = (max_length + 2)
    #     sheet.column_dimensions[column[0].column_letter].width = adjusted_width

    # response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    # current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    # response['Content-Disposition'] = f'attachment; filename=employees_{current_time}.xlsx'
    # workbook.save(response)
    return None