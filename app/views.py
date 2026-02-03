from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from .models import Asset, Employee, Assignment
from django.db.models import Q


class HomePageView(TemplateView):
    template_name = 'index.html'
class ListPageView(ListView):
    model = Asset
    template_name = 'index.html'

    def get_queryset(self):
        queryset = Asset.objects.all()

        query = self.request.GET.get('q')
        status_filter = self.request.GET.get('status')

        # 1. Handle Search
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(Asset_ID__icontains=query)
            )

        # 2. Handle Status Filter
        if status_filter == 'AVAIL':
            # Must be unassigned AND status must be 'AVAIL' (not REPAIR)
            queryset = queryset.filter(assigned_to__isnull=True, status='AVAIL')

        elif status_filter == 'BUSY':
            # Show only assets that HAVE a user assigned
            queryset = queryset.filter(assigned_to__isnull=False)

        elif status_filter == 'REPAIR':
            # Show only items explicitly marked as Under Repair
            queryset = queryset.filter(status='REPAIR')

        return queryset
class CreateAssetPageView(CreateView):
    model = Asset
    fields = ['name', 'category', 'assigned_to']
    template_name = 'add_asset.html'

class CreateEmployeePageView(CreateView):
    model = Employee
    fields = ['name', 'number', 'department', 'work_mode']
    template_name = 'add_employee.html'

class EmployeePageView(ListView):
    model = Employee
    context_object_name = 'emp'
    template_name = 'view_employee.html'

    def get_queryset(self):
        queryset = Employee.objects.all()

        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(employee_ID__icontains=query)
            )
        return queryset

class EmployeeDetailView(DetailView):
    model = Employee
    context_object_name = 'emp'
    template_name = 'employee_detail.html'

class AssetDetailView(DetailView):
    model = Asset
    template_name = 'asset_details.html'
    context_object_name = 'asset'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee_list'] = Employee.objects.all()
        return context

    # This handles the button clicks (Toggle Repair and Assign)
    def post(self, request, *args, **kwargs):
        asset = self.get_object()

        # If the Repair Toggle button was clicked
        if 'toggle_repair' in request.POST:
            if asset.status == 'REPAIR':
                asset.status = 'AVAIL'
            else:
                asset.status = 'REPAIR'
                asset.assigned_to = None  # Important: remove the holder
            asset.save()

        # If the Modal was used to assign an employee
        elif 'employee_id' in request.POST:
            if asset.status == 'REPAIR':
                # Don't allow assignment if status is repair
                return redirect('asset_details', pk=asset.pk)
            emp_id = request.POST.get('employee_id')
            asset.assigned_to = get_object_or_404(Employee, pk=emp_id)
            asset.save()  # This triggers the model's save() to set status to BUSY

        return redirect('asset_details', pk=asset.pk)

class LogListView(ListView):
    model = Assignment
    context_object_name = 'log'
    queryset = Assignment.objects.select_related('asset', 'employee').all()
    template_name = 'view_logs.html'

    def get_queryset(self):
        # Start with all logs, optimized with select_related
        queryset = Assignment.objects.select_related('asset', 'employee').all().order_by('-handover_date')

        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(asset__name__icontains=query) |  # Search Asset Name
                Q(asset__Asset_ID__icontains=query) |  # Search Asset ID
                Q(employee__name__icontains=query)  # Search Employee Name
            )
        return queryset

class UpdateAssetView(UpdateView):
    model = Asset
    fields = ['assigned_to']
    template_name = 'return_asset.html'

class EmployeeUpdateView(UpdateView):
    model = Employee
    fields = ['employee_ID', 'name', 'number', 'department', 'work_mode']
    template_name = 'employee_update.html'

class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = 'employee_delete.html'
    success_url = reverse_lazy('list_employee')





