from django.db import models
from datetime import timedelta
from django.contrib.auth.models import User

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
        try:
            #get the user's 1st period entry
            # previous_periods = PeriodTracker.objects.filter(user=self.user).order_by('start_date').first()
            # if previous_periods:
            #     #calculate the average cycle length based on the 1st entry
            #     cycle_length = (self.start_date - previous_periods.start_date).days
                
            #     #calculate the next period start date
            #     predicted_next_start = self.end_date + timedelta(days=cycle_length)
            #     self.next_period_start = predicted_next_start

            #     # Calculate the ovulation date (usually 14 days before the expected period)
            #     ovulation_date = predicted_next_start - timedelta(days=14)
            #     self.ovulation_date = ovulation_date

            cycles = PeriodTracker.objects.filter(user=self.user).order_by('-start_date')[:2]
            #check ensures that there are at least two period tracker entries available to calculate the next period and ovulation date. If there are not enough entries, the calculation won't be performed.
            if len(cycles) == 2:
                # we assign the most recent cycle (the first entry in the queryset) to last_cycle and the cycle before it (the second entry in the queryset) to previous_cycle.
                last_cycle = cycles[0]
                previous_cycle = cycles[1]
                # calculate cycle length
                cycle_length = (last_cycle.start_date - previous_cycle.start_date).days
                predicted_next_start = last_cycle.start_date + timedelta(days=cycle_length)
                last_cycle.next_period_start = predicted_next_start
 
                # Calculate the ovulation date (usually 14 days before the expected period).
                ovulation_date = predicted_next_start - timedelta(days=14)
                last_cycle.ovulation_date = ovulation_date
                last_cycle.save()
            
        except Exception as e:
            # Handle any errors or exceptions here
            pass
    
    def __str__(self):
        return f'Period Tracker for {self.user.username},{self.user.id}'
    
class SymptomLog(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateField()
    mood_swings = models.BooleanField(default=False)
    cramps = models.BooleanField(default=False)
    headache = models.BooleanField(default=False)
    backpain = models.BooleanField(default=False)
    food_cravings = models.BooleanField(default=False)
    vomiting = models.BooleanField(default=False)
    irritation = models.BooleanField(default=False)
    spotting = models.BooleanField(default=False)
    additional_info = models.TextField(blank=True, null=True)
    
    