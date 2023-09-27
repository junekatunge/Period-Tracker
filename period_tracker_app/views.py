from django.shortcuts import render
from .models import *
import lunarcalendar
# Create your views here.
#view for displaying the period data and additional sysmptoms


def predict_next_period(period_tracker):
    next_period = lunarcalendar.get_next_period(period_tracker.start_date, period_tracker.cycle_length)
    return next_period

def predict_next_ovulation(period_tracker):
    next_ovulation = lunarcalendar.get_next_ovulation(period_tracker.start_date, period_tracker.cycle_length)
    return next_ovulation

def period_tracker_view (request):
    period_trackers = PeriodTracker.objects.filter(user=request.user)
    
    
    
    context = {
        'period_trackers':period_trackers
    }
    
    return render(request,'period_tracker/period_tracker.html',context)