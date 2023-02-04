from django.db import models
from django.db.models import Q
from accounts.models import User


class ExperienceLevel(models.IntegerChoices):
    BEGINNER = 0, 'Beginner'
    INTERMEDIATE = 1, 'Intermediate'
    EXPERT = 2, 'Expert'


class Benefactor(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='benefactor')
    experience = models.SmallIntegerField(
        choices=ExperienceLevel.choices, default=ExperienceLevel.BEGINNER)
    free_time_per_week = models.PositiveSmallIntegerField(default=0)


class Charity(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='charity')
    name = models.CharField(max_length=50)
    reg_number = models.CharField(max_length=10)


class TaskManager(models.Manager):
    def related_tasks_to_charity(self, user: User):
        user_charity = user.charity
        queryset = Task.objects.filter(charity=user_charity)
        return queryset

    def related_tasks_to_benefactor(self, user: User):
        user_benefactor = user.benefactor
        queryset = Task.objects.filter(assigned_benefactor=user_benefactor)
        return queryset

    def all_related_tasks_to_user(self, user: User):
        user_charity = user.charity
        user_benefactor = user.benefactor
        queryset = Task.objects.filter(Q(charity=user_charity)
                                       | Q(assigned_benefactor=user_benefactor)
                                       | Q(state='P'))
        return queryset


class Task(models.Model):
    objects = TaskManager()

    GENDER_CHOICES = (
        ('F', 'Female'),
        ('M', 'Male'),
    )

    STATE_CHOICES = (
        ('P', 'Pending'),
        ('W', 'Waiting'),
        ('A', 'Assigned'),
        ('D', 'Done'),
    )

    assigned_benefactor = models.ForeignKey(
        Benefactor, null=True, on_delete=models.SET_NULL, related_name='task')
    charity = models.ForeignKey(
        Charity, on_delete=models.CASCADE, related_name='task')
    age_limit_from = models.IntegerField(blank=True, null=True)
    age_limit_to = models.IntegerField(blank=True, null=True)
    data = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    gender_limit = models.CharField(
        max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    state = models.CharField(max_length=1, choices=STATE_CHOICES, default='P')
    title = models.CharField(max_length=60)
