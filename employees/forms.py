from django import forms
from .models import Employee
from .models import Leave

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'


# class LeaveForm(forms.ModelForm):
#     class Meta:
#         model = Leave
#         fields = ['employee', 'leave_type', 'start_date', 'end_date', 'reason']
        
#     def clean(self):
#         cleaned_data = super().clean()
#         employee = cleaned_data.get('employee')
#         start_date = cleaned_data.get('start_date')
#         end_date = cleaned_data.get('end_date')
        
#         if employee and start_date and end_date:
#             total_leaves_taken = Leave.objects.filter(
#                 employee=employee,
#                 start_date__year=start_date.year,
#                 end_date__year=end_date.year
#             ).count()
            
#             if total_leaves_taken >= 28:
#                 raise forms.ValidationError("The employee has already taken the maximum number of leaves for this year.")



# from django import forms
# from .models import Leave

class AddLeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['employee', 'start_date', 'end_date', 'reason', 'leave_type',]
