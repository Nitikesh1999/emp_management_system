from django.db import models
from datetime import timedelta

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    leave_balance=models.PositiveIntegerField(editable=False,default=28)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_remaining_leaves(self):
        pending_leave = PendingLeave.objects.get(employee=self)
        return pending_leave.remaining_leaves    
    
    


class Leave(models.Model):
    LEAVE_TYPE_CHOICES = (
        ('sick_leave', 'Sick Leave'),
        ('vacation', 'Vacation'),
        ('other_leave', 'Other Leave'),
    )
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    def __str__(self):
        return f"Leave #{self.id} - Employee: {self.employee}"
    


class PendingLeave(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    remaining_leaves = models.PositiveIntegerField(default=28)

    def get_total_duration(self):
        leaves_taken = Leave.objects.filter(employee=self.employee)
        total_duration = sum((leave.end_date - leave.start_date).days for leave in leaves_taken)
        return total_duration

    def save(self, *args, **kwargs):
        total_duration = self.get_total_duration()
        self.remaining_leaves = 28 - total_duration
        super().save(*args, **kwargs)
