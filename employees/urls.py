from django.urls import path
from .views import add_employee, employee_list ,add_leave, pending_leave_record
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('add-employee/', add_employee, name='add_employee'),
    path('employee-list/', employee_list, name='employee_list'),
    path('update-employee/<int:pk>/', views.update_employee, name='update_employee'),
    path('delete-employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    path('employee-leaves/', add_leave, name='add_leave'),
        path('leave-pending/', pending_leave_record, name='pending_leave_record'),



    
]
