from django.urls import path, include
from rest_framework import routers
from accounts.views.api_views import LogInViewSets, SignUpViewSets, UserViewSet, GetUserOnlyViewSet

router = routers.DefaultRouter()
router.register('login', LogInViewSets, basename='log_in')
router.register('signup', SignUpViewSets, basename='sign_up')
router.register('employee-detail', UserViewSet, basename='employee_detail')
router.register('get-employee-only', GetUserOnlyViewSet, basename='employee_detail')

# urlpatterns = [
#     path('', include(router.urls)),
# ]
urlpatterns = [

    path('', include(router.urls)),
    # path('create-task/',  api_views.TaskViewSet.as_view(), name="create_task"),
]


