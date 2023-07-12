from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import EmployeeForm
from .models import Employee,Leave, PendingLeave
from .forms import AddLeaveForm
from datetime import timedelta
from django.db.models import Sum



def base(request):
    return render(request, 'employees/base.html')

def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employees/add_employee.html', {'form': form})

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees': employees})

def update_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'employees/update_employee.html', {'form': form})


def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')

    return redirect('employee_list')

from datetime import datetime, timedelta

def add_leave(request):
    if request.method == 'POST':
        form = AddLeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            employee = form.cleaned_data['employee']
            
            # Calculate the total duration of the leave
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            total_duration = (end_date - start_date).days + 1  # Add 1 day to include both start and end dates
            
            # Update the remaining leaves of the employee
            pending_leave, created = PendingLeave.objects.get_or_create(employee=employee)
            pending_leave.remaining_leaves -= total_duration
            pending_leave.save()
            
            # Save the leave with the calculated duration
            leave.total_duration = total_duration
            leave.save()
            
            return redirect('pending_leave_record')
    else:
        form = AddLeaveForm()
        employees = Employee.objects.all()

    return render(request, 'employees/add_leave.html', {'form': form, 'employees': employees})

def pending_leave_record(request):
    pending_leaves = PendingLeave.objects.all()
    for pending_leave in pending_leaves:
        leaves_taken = Leave.objects.filter(employee=pending_leave.employee)
        total_duration = sum((leave.end_date - leave.start_date).days for leave in leaves_taken)
        remaining_leaves = 28 - total_duration
        pending_leave.remaining_leaves = remaining_leaves
        pending_leave.save()
    return render(request, 'employees/pending_leave_record.html', {'pending_leaves': pending_leaves})

