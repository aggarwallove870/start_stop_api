from django.urls import path, include
from flexoffice_app.views import views

urlpatterns = [

    path('', views.dashboard, name='dashboard'),
    path('attendance/', views.attendance, name='attendance'),
    path('employee-list/', views.employeelist,  name='employeelist'),
    path('calculate-salary/', views.calculatesalary, name='calculatesalary'),
    path('month-attendance/', views.attendancelist ,  name='attendancelist'),
    path('addnote/', views.addnote, name='addnote'),
    path('mailsalary/', views.mailsalary, name='mailsalary'),
    path('salary-history', views.salaryhistory, name='salaryhistory'),
    path('report', views.morning_report, name='morning_report'),
    path('reports/all', views.reports_all, name='reports_all'),
    path('employee/add', views.employee_add, name='employee_add'),

    path('viewimage/', views.image, name='image'),

]
