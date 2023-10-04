from django.db import models
from datetime import timedelta

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
    next_period_start = models.DateField(null=True, blank=True)
    ovulation_date = models.DateField(null=True, blank=True)
    
    def calculate_next_period_and_ovulation(self):
        try:#calculatee the latest cycle length based on the previous entry
            previous_periods = PeriodTracker.objects.filter(user=self.user).exclude(id = self.id).order_by('start_date').first()
            if previous_periods:
                cycle_length = (self.start_date - previous_periods.start_date).days
                predicted_next_start = self.start_date + timedelta(days=cycle_length)
                self.next_period_start = predicted_next_start

                # Calculate the ovulation date (usually 14 days before the expected period)
                ovulation_date = predicted_next_start - timedelta(days=14)
                self.ovulation_date = ovulation_date

                self.save()
        except Exception as e:
            # Handle any errors or exceptions here
            pass
    
    def __str__(self):
        return f'Period Tracker for {self.user.username},{self.user.id}'
    