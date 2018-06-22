from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class ContractsManager(models.Manager):
    def get_queryset(self):
        return super(ContractsManager, self).get_queryset().filter(project_status='approved')

class Contract(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    )
    client_name = models.CharField(max_length=80)
    project_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique_for_date='project_publish_date')
    project_lead = models.ForeignKey(User, related_name='project_publish_date')
    project_status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='pending')
    project_description = models.TextField()
    project_publish_date = models.DateTimeField(default=timezone.now)

    objects = models.Manager()  # This is the default manager
    approved = ContractsManager()  # The specific manager

    class Meta:
        ordering = ('-project_publish_date',)

    def __str__(self):
        return self.project_name

    def get_absolute_url(self):
        return reverse('contract:contract_detail', args=[self.project_publish_date.year,
                                                        self.project_publish_date.strftime('%m'),
                                                        self.project_publish_date.strftime('%d'),
                                                        self.slug])


