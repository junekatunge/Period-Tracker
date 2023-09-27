from django.urls import path
from period_tracker_app.views import period_tracker_view





urlpatterns = [
    path('',period_tracker_view,name = 'period_tacker')
]