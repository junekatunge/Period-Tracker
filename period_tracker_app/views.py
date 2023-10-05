from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from datetime import timedelta

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
        #calculate  and update the predicted next period and ovulation date
        # cycles = PeriodTracker.objects.filter(user=request.user).order_by('-start_date')[:2]
        # if len(cycles) == 2:
        #     last_cycle = cycles[0]
        #     previous_cycle = cycles[1]
        #     cycle_length = (last_cycle.start_date - previous_cycle.start_date).days
        #     predicted_next_start = last_cycle.start_date + timedelta(days=cycle_length)
        #     last_cycle.next_period_start = predicted_next_start

        #     # Calculate the ovulation date (usually 14 days before the expected period).
        #     ovulation_date = predicted_next_start - timedelta(days=14)
        #     last_cycle.ovulation_date = ovulation_date
        #     last_cycle.save()
        first_period_entry = PeriodTracker.objects.filter(user=request.user).order_by('start_date').first()

        if first_period_entry:
        # Calculate the next period and ovulation date based on the first entry
            first_period_entry.calculate_next_period_and_ovulation()
            return redirect(view_period_tracker)  # Redirect to view page after calculation

    return render(request,'period_tracker/add_period_tracker.html')  # Redirect even if no entry is found

    # else:
    #     return render(request,'period_tracker/add_period_tracker.html')

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

# view for loging in the daily symptoms

def log_symptoms(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        selected_symptoms = request.POST.getlist('symptoms')
        additional_info = request.POST.get('additional_info','')
        
        for symptom in selected_symptoms:
            SymptomLog.objects.create(
                user=request.user,
                date=date,
                symptoms=symptom,
                additional_info=additional_info
            )
        return redirect('view_symptom_logs')

    return render(request, 'period_tracker/log_symptoms.html')
        