# urls.py
from django.urls import path

from finish import settings

# from dashboard.viewsf.pdf_views import IDCardView
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('home',views.home_page,name='home'),
    path('login',views.login_page,name='login'),
    path('logout',views.logout_page,name='logout'),
    path('add_event/', views.add_event, name='add_event'),
    path('Upcoming_Events', views.upcoming_events, name='upcoming_events'),
    path('Ongoing_Events', views.ongoing_events, name='ongoing_events'),
    path('All_Events',views.all_events,name='all_events'),  
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('settings/', views.settings_page, name='settings'),
    path('add_venue/',views.add_venue,name="add_venue"),
    path('venue_list/',views.venue_list,name='venue_list'),
    path('edit_venue/<eid>',views.edit_venue,name='edit_venue'),
    path('delete_venue/<vid>',views.delete_venue,name='delete_venue'),
    path('delete_client/<cid>',views.delete_client),
    path('add_client/',views.add_client),
    path('update_client/<cid>',views.update_client),
    path('client_detail/',views.client_detail),
    path('update_client/cid',views.update_client),
    path('update_event/<eid>',views.update_event),
    path('Employee_List/',views.employee_list),
    path('Add_Employees/',views.add_employee),
    path('Update_Employee/<eid>',views.update_employee),
    path('Add_Interns/',views.add_intern),
    path('employee_detail/<eid>',views.employee_detail),
    path('Intern_List/',views.intern_list),
    path('profile/',views.profile),
    path('problemreport/',views.report_problem),
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
    path('lead_entry/', views.LeadEntry, name='lead_entry'),
    path('lead_list/', views.LeadList, name='lead_list'),
    path('converted_leads/',views.ConvertedLeads,name='converted-leads'),
    path('cancel_leads/',views.LeadCancel,name='cancel-leads'),
    path('mark_attendance/',views.mark_attendance,name="mark-attendance"),
    path('convert/<int:lid>/', views.convert_lead, name='convert_lead'),
    path('reject/<int:lid>/', views.reject_lead, name='reject_lead'),
    path('certificate_form', views.certificate_form, name='certificate_form'),
    path('generate_pdf/', views.generate_certificate, name='generate_pdf'),
    path('event_detail/<int:eid>/', views.event_detail, name='event_detail'),
    path('add_expense/<int:eid>/', views.add_expense, name='add_expense'),
    path('update_leads/<lead_id>/',views.UpdateLead,name='update_lead'),
    path('lead_list/<lead_id>/',views.leaddetail),
    path('check',views.check),
    path('change-theme/', views.change_theme, name='change-theme'),
    path('change-language/', views.change_language, name='change_language')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)