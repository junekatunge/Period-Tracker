from django.urls import path
from period_tracker_app.views import add_period_tracker,view_period_tracker,update_period_tracker,delete_period_tracker





urlpatterns = [
    path('',add_period_tracker,name = 'period_tacker'),
    path('period_tracker/add/',add_period_tracker, name = 'add_period_tracker'),
    path('period_tracker/view/',view_period_tracker,name ='period_tracker_view'),
    path('period_tracker/update/<int:entry_id>/',update_period_tracker,name= 'update_period_tracker'),
    path('period_tracker/delete/<int:entry_id>/', delete_period_tracker, name='delete_period_tracker')
    
]
