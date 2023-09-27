from django.db import models

# Create your models here.
class PeriodTracker(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    cycle_length = models.IntegerField()
    mood_swings = models.BooleanField()
    cramps = models.BooleanField()
    breast_tenderness = models.BooleanField()
    headaches = models.BooleanField()
    back_pain = models.BooleanField()
    food_cravings = models.BooleanField()
    
    def __str__(self):
        return f'Period Tracker for {self.user}'
    