from django.urls import path, include
from rest_framework import routers
from flexoffice_app.views.api_views import AttendanceSheetViewSet, AttendanceViewSet, AttendanceDetailViewSet, \
    SalaryViewSet, SalaryBonusViewSet

router = routers.DefaultRouter()
router.register('attendance-sheet', AttendanceSheetViewSet, basename='attendance_sheet')
router.register('attendance', AttendanceViewSet, basename='attendance')
router.register('attendance-detail', AttendanceDetailViewSet, basename='attendance_detail')
router.register('salary', SalaryViewSet, basename='salary')
router.register('salary-bonus', SalaryBonusViewSet, basename='salary_bonus')

urlpatterns = [

    path('', include(router.urls)),
    # path('create-task/',  api_views.TaskViewSet.as_view(), name="create_task"),
]


