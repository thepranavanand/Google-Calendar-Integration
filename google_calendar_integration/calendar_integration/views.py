from django.shortcuts import render

# Create your views here.
from googleapiclient.discovery import build
from django.http import HttpResponse
from django.views import View
from google_auth_oauthlib.flow import InstalledAppFlow
from django.shortcuts import HttpResponseRedirect


class GoogleCalendarInitView(View):
    def get(self, request):
        client_id = '787350811108-gie6j26s9t3ashgk75i675l6ok8pt5v5.apps.googleusercontent.com'
        client_secret = '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'
        scopes = ['https://www.googleapis.com/auth/calendar.readonly']

        flow = InstalledAppFlow.from_client_secrets_file(
            'google_calendar_integration/CloudCreds/client_secrets.json',
            scopes=scopes,
            
redirect_uri = 'https://Google-Calendar-Integration.thepranavanand.repl.co/rest/v1/calendar/redirect/'

        )

        authorization_url, state = flow.authorization_url(prompt='consent')

        request.session['oauth_state'] = state

        return HttpResponseRedirect(authorization_url)

class GoogleCalendarRedirectView(View):
    def get(self, request):
        code = request.GET.get('code')
        state = request.GET.get('state')

        stored_state = request.session.pop('oauth_state', None)
        if state != stored_state:
            return HttpResponse('Invalid state parameter.', status=400)

        flow = InstalledAppFlow.from_client_secrets_file(
            'google_calendar_integration/CloudCreds/client_secrets.json',
            scopes=['https://www.googleapis.com/auth/calendar.readonly'],
            redirect_uri='https://Google-Calendar-Integration.thepranavanand.repl.co/rest/v1/calendar/redirect/'
        )
        flow.fetch_token(code=code)

        credentials = flow.credentials
        access_token = credentials.token

        service = build('calendar', 'v3', credentials=credentials)

        events_result = service.events().list(calendarId='primary').execute()
        events = events_result.get('items', [])

        return JsonResponse(events, safe=False)
