from django.db import models
from django.db.models import Q


class Branch(models.Model):
    name = models.CharField(max_length=120, unique=True)
    city = models.CharField(max_length=80)
    address = models.CharField(max_length=255)
    opened_year = models.IntegerField(null=True, blank=True)
    is_open = models.BooleanField(default=True)

    class Meta:
        db_table = 'branches'
        ordering = ['city', 'name']
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'
        indexes = [
            models.Index(fields=['city'], name='idx_branch_city'),
            models.Index(
                fields=['city', 'name'],
                name='idx_open_branches',
                condition=Q(is_open=True),
            ),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(name__gt=''),
                name='branch_name_not_empty',
            ),
            models.CheckConstraint(
                condition=Q(opened_year__isnull=True) | Q(opened_year__gte=1990, opened_year__lte=2026),
                name='branch_opened_year_valid',
            ),
        ]

    def __str__(self):
        return f'{self.name} ({self.city})'


class Employee(models.Model):
    full_name = models.CharField(max_length=150)
    position = models.CharField(max_length=100)
    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees',
    )
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'employees'
        ordering = ['full_name']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        indexes = [
            models.Index(fields=['branch'], name='idx_employee_branch'),
            models.Index(fields=['-salary'], name='idx_employee_salary_desc'),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(full_name__gt=''),
                name='employee_name_not_empty',
            ),
            models.CheckConstraint(
                condition=Q(salary__gte=0),
                name='employee_salary_non_negative',
            ),
        ]

    def __str__(self):
        return f'{self.full_name} — {self.position}'


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='news_posts',
    )
    published_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        db_table = 'company_news'
        ordering = ['-published_at']
        verbose_name = 'News'
        verbose_name_plural = 'News'
        indexes = [
            models.Index(fields=['-published_at'], name='idx_news_published_desc'),
            models.Index(
                fields=['-published_at'],
                name='idx_active_news',
                condition=Q(is_published=True),
            ),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(title__gt=''),
                name='news_title_not_empty',
            ),
        ]

    def __str__(self):
        return self.title


class IceCreamDonation(models.Model):
    donor_name = models.CharField(max_length=100, default='Аноним')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    ice_cream_flavor = models.CharField(max_length=80, blank=True, default='Пломбир')
    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='donations',
    )
    donated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ice_cream_donations'
        ordering = ['-donated_at']
        verbose_name = 'Ice Cream Donation'
        verbose_name_plural = 'Ice Cream Donations'
        indexes = [
            models.Index(fields=['-amount'], name='idx_donation_amount_desc'),
            models.Index(fields=['-donated_at'], name='idx_donation_date_desc'),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(amount__gt=0),
                name='donation_amount_positive',
            ),
        ]

    def __str__(self):
        return f'{self.donor_name}: +{self.amount} ({self.ice_cream_flavor})'


class Task(models.Model):
    title = models.CharField(max_length=200)
    assignee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='tasks',
    )
    priority = models.IntegerField(default=1)
    deadline = models.DateField(null=True, blank=True)
    is_done = models.BooleanField(default=False)

    class Meta:
        db_table = 'tasks'
        ordering = ['is_done', '-priority', 'deadline']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        indexes = [
            models.Index(fields=['assignee', 'is_done'], name='idx_task_assignee_status'),
            models.Index(
                fields=['deadline'],
                name='idx_pending_tasks_deadline',
                condition=Q(is_done=False, deadline__isnull=False),
            ),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(title__gt=''),
                name='task_title_not_empty',
            ),
            models.CheckConstraint(
                condition=Q(priority__gte=1) & Q(priority__lte=5),
                name='task_priority_range',
            ),
        ]

    def __str__(self):
        return self.title