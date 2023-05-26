from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from google.oauth2 import credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CLIENT_SECRET_FILE = "C:\\Users\\Lenovo\\Desktop\\Google_Calendar_Django\\google_calendar_integration\\client_secret_82032754664-qgdu8ltsodhm9bt7roa920ve94co16tg.apps.googleusercontent.com.json"


class GoogleCalendarInitView(View):
    def get(self, request):
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
        #credentials = flow.run_console()
        authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
        request.session['state'] = state
        return HttpResponseRedirect(authorization_url)


class GoogleCalendarRedirectView(View):
    def get(self, request):
        state = request.session.pop('state', '')
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES, state=state)
        flow.fetch_token(authorization_response=request.build_absolute_uri())
        credentials = flow.credentials
        service = build('calendar', 'v3', credentials=credentials)
        events_result = service.events().list(calendarId='primary', maxResults=10).execute()
        events = events_result.get('items', [])
        if not events:
            response = "No events found."
        else:
            response = "Upcoming events:\n"
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                response += f"- {start} - {event['summary']}\n"
        return HttpResponse(response)

