from django.db import models


class CustomSchedule(models.Model):
    REPEAT_CHOICES = [
        ('N', 'Never'),
        ('D', 'Daily'),
        ('W', 'Weekly'),
        ('M', 'Monthly'),
        ('Y', 'Yearly'),
    ]

    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    description = models.TextField(default='', blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(default=None, null=True, blank=True)
    repeat = models.CharField(
        max_length=50,
        choices=REPEAT_CHOICES,
        default='N'
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.start_time.strftime('%H:%M:%S')} {self.name}"
