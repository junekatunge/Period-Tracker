from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from datetime import timedelta
from django.db.models import Q
from django.http import HttpResponse
from datetime import datetime,timezone
import pytz

def view_period_tracker(request):
    period_entries = PeriodTracker.objects.filter(user=request.user).order_by('-start_date')
    
    context = {
        'period_entries' : period_entries
    }
    return render(request,'period_tracker/period_tracker_view.html',context)
#adding the period details
def add_period_tracker(request):
    if request.method == 'POST':
        # Process the form data and save the period tracker entry.
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        cycle_length = request.POST['cycle_length']
        mood_swings = request.POST.get('mood_swings', False) == "true"
        cramps = request.POST.get('cramps', False)== "true"
        breast_tenderness = request.POST.get('breast_tenderness', False)== "true"
        headaches = request.POST.get('headaches', False)== "true"
        back_pain = request.POST.get('back_pain', False)== "true"
        food_cravings = request.POST.get('food_cravings', False)== "true"
        
        period_tracker = PeriodTracker(
            user=request.user,
            start_date=start_date,
            end_date=end_date,
            cycle_length=cycle_length,
            mood_swings=mood_swings,
            cramps=cramps,
            breast_tenderness=breast_tenderness,
            headaches=headaches,
            back_pain=back_pain,
            food_cravings=food_cravings,
        )
        period_tracker.save()
      
        first_period_entry = PeriodTracker.objects.filter(user=request.user).order_by('start_date').first()

        if first_period_entry:
        # Calculate the next period and ovulation date based on the first entry
            first_period_entry.calculate_next_period_and_ovulation()
            return redirect(view_period_tracker)  # Redirect to view page after calculation

    return render(request,'period_tracker/add_period_tracker.html')  # Redirect even if no entry is found

 

def update_period_tracker(request,entry_id):
    entry = get_object_or_404(PeriodTracker,id=entry_id, user=request.user)
    
    if request.method == 'POST':
        # Process the form data and update the period tracker entry.
        entry.start_date = request.POST.get('start_date','')
        entry.end_date = request.POST.get('end_date','')
        entry.cycle_length = request.POST.get('cycle_length','')
        entry.mood_swings = request.POST.get('mood_swings', False) == "true"
        entry.cramps = request.POST.get('cramps', False) == "true"
        entry.breast_tenderness = request.POST.get('breast_tenderness', False) == "true"
        entry.headaches = request.POST.get('headaches', False) == "true"
        entry.back_pain = request.POST.get('back_pain', False) == "true"
        entry.food_cravings = request.POST.get('food_cravings', False) == "true"
        
        entry.save()
        
        return redirect(view_period_tracker)  # Redirect to view page after updating

    context = {
        'entry': entry,
    }

    return render(request, 'period_tracker/update_period_tracker.html', context)
    
def delete_period_tracker(request, entry_id):
    entry = get_object_or_404(PeriodTracker, id=entry_id, user=request.user)
    
    if request.method == 'POST':
        entry.delete()
        return redirect(view_period_tracker)  # Redirect to view page after deleting

    context = {
        'entry': entry,
    }

    return render(request, 'period_tracker/delete_period_tracker.html', context)


# view for viewing the logged daily symptoms
def view_symptom_logs(request):
    symptom_logs = SymptomLog.objects.filter(user=request.user).order_by('-date')
    return render(request,'period_tracker/view_symptom_logs.html',{'symptom_logs': symptom_logs})
    
from django.utils import timezone

# log symptoms
def log_symptoms(request):
    if request.method == 'POST':
        print(request.POST)
        date_str = request.POST.get('date')
        additional_info = request.POST.get('additional_info', '')

        # Convert the date string to a datetime object
        date = timezone.make_aware(timezone.datetime.strptime(date_str, "%Y-%m-%d"))

        # Check if the entered date is in the future
        # today = timezone.now().date()
        current_datetime = datetime.now(pytz.timezone('US/Eastern'))
        if date > current_datetime:
            return HttpResponse("Cannot log symptoms for future dates.")

        # Check if a symptom log entry for the specified date and user exists
        existing_log, created = SymptomLog.objects.get_or_create(date=date, user=request.user, defaults={'additional_info': additional_info})

        # Define a list of symptom field names
        symptom_fields = ['mood_swings', 'cramps', 'headache', 'backpain', 'food_cravings', 'vomiting', 'irritation', 'spotting']

        # Loop through the symptom field names to set values to True or False
        for field in symptom_fields:
            setattr(existing_log, field, request.POST.get(field) == 'on')

        existing_log.additional_info = additional_info
        existing_log.save()

        return redirect('view_symptom_logs')

    # If you haven't logged the symptoms, render the form
    return render(request, 'period_tracker/log_symptoms.html')


        