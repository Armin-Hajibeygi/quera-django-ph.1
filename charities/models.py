from django.db import models


class Benefactor(models.Model):
    pass


class Charity(models.Model):
    pass


class Task(models.Model):
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
        Benefactor, null=True, on_delete=models.SET_NULL)
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE)
    age_limit_from = models.IntegerField(blank=True, null=True)
    age_limit_to = models.IntegerField(blank=True, null=True)
    data = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    gender_limit = models.CharField(
        max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    state = models.CharField(max_length=1, choices=STATE_CHOICES, default='P')
    title = models.CharField(max_length=60)
