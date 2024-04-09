from django.contrib import admin
from .models import CustomUser, WorkLog, Client, Venue, Event, Sales, Expenses, GoodsList, EventExcel, EmployeeExcel, DocumentOfEmployee, UserSettings, Attendance, Lead, ProblemOfEmployee

admin.site.register(CustomUser)
admin.site.register(WorkLog)
admin.site.register(Client)
admin.site.register(Venue)
admin.site.register(Event)
admin.site.register(Sales)
admin.site.register(Expenses)
admin.site.register(GoodsList)
admin.site.register(EventExcel)
admin.site.register(EmployeeExcel)
admin.site.register(DocumentOfEmployee)
admin.site.register(UserSettings)
admin.site.register(Attendance)
admin.site.register(Lead)
admin.site.register(ProblemOfEmployee)
