from django.urls import path
from .views import *

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    path('add_user/', add_user, name='add_user'),
    path('view_user/<int:user_id>/', view_user, name='view_user'),
    path('edit_user/<int:user_id>/', edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('staffs/', view_staffs, name='view_staffs'),

    path('add_report/', add_report, name='add_report'),
    path('view_report/<int:report_id>/', view_report, name='view_report'),
    path('edit_report/<int:report_id>/', edit_report, name='edit_report'),
    path('delete_report/<int:report_id>/', delete_report, name='delete_report'),

    path('reports/', reports_staff_view, name='reports_staff_view'),

    path('manager/home/', manager_home_view, name='manager_home'),
    path('reports_manager_view/', reports_manager_view, name='reports_manager_view'),
    path('reports/approve/<int:report_id>/', approve_report, name='approve_report'),
    path('reports/reject/<int:report_id>/', reject_report, name='reject_report'),
]