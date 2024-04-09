from django.http import HttpResponse
from django.shortcuts import render, redirect
from ..models import CustomUser, Attendance, WorkLog
from django.utils import timezone
from datetime import datetime, timedelta

def mark_attendance(request):
    # Check if the user is a manager
    if not request.user.is_authenticated or request.user.category != 'manager':
        return redirect('access_denied_url')  # Redirect unauthorized users

    current_time = datetime.now().time()  # Get current time

    if request.method == 'POST':
        # Check if the current time is within the allowed attendance marking window
        if current_time <= datetime.strptime('12:00', '%H:%M').time():
            # Get the selected shift from the form
            shift = request.POST.get('shift')

            # Get the IDs of employees who marked themselves present
            present_employee_ids = request.POST.getlist('present_employee')

            # Mark employees present
            for employee_id in present_employee_ids:
                Attendance.objects.create(
                    user_id=employee_id,
                    datetime=timezone.now(),
                    shift=shift,
                    status='present'
                )

            return HttpResponse("attendance mark successfully")  # Redirect to success page after marking attendance
        else:
            return HttpResponse('attendance_time_expired_url')  # Redirect if time for marking attendance has expired

    # Query employees and their shift information
    employees = CustomUser.objects.filter(category='employee')
    shift_information = {}  # Dictionary to store shift information for each employee

    for employee in employees:
        # Assuming WorkLog model stores information about employee shifts
        employee_shifts = WorkLog.objects.filter(employee=employee)
        shift_information[employee.id] = employee_shifts

    return render(request, 'mark_attendance.html', {'employees': employees, 'shift_information': shift_information, 'current_time': current_time})
