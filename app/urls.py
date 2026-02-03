from django.urls import path

from .views import ListPageView, CreateAssetPageView, CreateEmployeePageView, AssetDetailView, \
    LogListView, EmployeeDetailView, EmployeePageView, UpdateAssetView, EmployeeUpdateView, EmployeeDeleteView

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('', ListPageView.as_view(), name = 'list_view'),
    path('list/create_asset', CreateAssetPageView.as_view(), name = 'add_asset'),
    path('list/create_employee', CreateEmployeePageView.as_view(), name = 'add_employee'),
    path('list/asset/<int:pk>', AssetDetailView.as_view(), name = 'asset_details'),
    path('list/log', LogListView.as_view(), name = 'view_log'),
    path('employee_list', EmployeePageView.as_view(), name = 'list_employee'),
    path('employee/<int:pk>', EmployeeDetailView.as_view(), name = 'employee_details'),
    path('list/asset/<int:pk>/update', UpdateAssetView.as_view(), name = 'assign_asset'),
    path('list/employee/<int:pk>/update', EmployeeUpdateView.as_view(), name = 'employee_update'),
    path('list/employee/<int:pk>/delete', EmployeeDeleteView.as_view(), name = 'employee_delete'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]