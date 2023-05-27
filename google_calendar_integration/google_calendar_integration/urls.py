
from django.contrib import admin
from django.urls import path
from calendar_integration.views import GoogleCalendarInitView, GoogleCalendarRedirectView

urlpatterns = [
    path('', GoogleCalendarInitView.as_view(), name='home'),
    path('rest/v1/calendar/init/', GoogleCalendarInitView.as_view(), name='calendar-init'),
    path('rest/v1/calendar/redirect/', GoogleCalendarRedirectView.as_view(), name='calendar-redirect'),
    path('admin/', admin.site.urls),
]