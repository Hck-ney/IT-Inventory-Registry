from django.urls import reverse
from django.utils import timezone

from django.db import models
from django.views.generic import UpdateView


class Employee(models.Model):
    mode_choices = [
        ('SITE', 'On-Site'), ('WFH', 'Work From Home')
    ]
    employee_ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    number = models.CharField(max_length=11)
    department = models.CharField(max_length=255)
    work_mode = models.CharField(choices=mode_choices, default='SITE', max_length=4)

    def __str__(self):
        return f"{self.name} ({self.department})"

    def get_absolute_url(self):
        return reverse('employee_details', kwargs={'pk': self.pk})


class Asset(models.Model):
    STATUS_CHOICES = [('AVAIL', 'Available'), ('BUSY', 'Assigned'), ('REPAIR', 'Under Repair')]
    ASSET_CATEGORIES = [
        ('LP', 'Laptop'),
        ('MONITOR', 'Monitor'),
        ('SU', 'System Unit'),
        ('MOUSE', 'Mouse'),
        ('KB', 'Keyboard')
    ]

    name = models.CharField(max_length=255)
    Asset_ID = models.AutoField(primary_key=True)
    category = models.CharField(choices=ASSET_CATEGORIES, max_length=10)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='AVAIL')
    assigned_to = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='current_assets',
    )

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        # 1. Sync status based on assignment
        if self.assigned_to:
            self.status = 'BUSY'
        elif self.status == 'REPAIR':
            # Keep it as REPAIR if it's already tagged as such
            pass
        else:
            # Only default to AVAIL if there is no user AND it's not in repair
            self.status = 'AVAIL'

        if not is_new:
            old_asset = Asset.objects.get(pk=self.pk)
            if old_asset.assigned_to != self.assigned_to:
                # Handle returning the old assignment
                if old_asset.assigned_to:
                    Assignment.objects.filter(
                        asset=self,
                        employee=old_asset.assigned_to,
                        return_date__isnull=True
                    ).update(return_date=timezone.now())

                # Handle creating the new assignment
                if self.assigned_to:
                    Assignment.objects.create(
                        asset=self,
                        employee=self.assigned_to,
                        handover_date=timezone.now()
                    )

        super().save(*args, **kwargs)

        # 2. Handle the Log for a brand new Asset
        if is_new and self.assigned_to:
            Assignment.objects.create(
                asset=self,
                employee=self.assigned_to,
                handover_date=timezone.now()
            )

    @property
    def current_user_name(self):
        return self.assigned_to.name if self.assigned_to else "Unassigned"

    def __str__(self):
        return f"{self.name} [{self.status}]"

    def get_absolute_url(self):
        return reverse('asset_details', kwargs={'pk': self.pk})


class Assignment(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='history')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='history')
    handover_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Log: {self.asset.name} to {self.employee.name}"

