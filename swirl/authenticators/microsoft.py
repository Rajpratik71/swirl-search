import msal
from django.http import HttpResponseRedirect
import requests
from datetime import datetime
from swirl.authenticators.authenticator import Authenticator
from django.conf import settings
from django.shortcuts import redirect

scopes = ["User.Read", "Mail.Read", "Files.Read.All", "Calendars.Read", "Sites.Read.All", "Chat.Read"]

graph_url = 'https://graph.microsoft.com/v1.0'

class Microsoft(Authenticator):

    type = "SWIRL Microsoft Authenticator"

    ########################################

    def __init__(self):
        self.access_token_field = 'microsoft_access_token'
        self.refresh_token_field = 'microsoft_refresh_token'
        self.expires_in_field = 'microsoft_access_token_expiration_time'

    def get_user(self, token):
        user = requests.get('{0}/me'.format(graph_url),
            headers={'Authorization': 'Bearer {0}'.format(token)},
            params={
                '$select': 'displayName,mail,userPrincipalName'
            })
        return user.json()

    def store_user(self, request, user, result):
        try:
            now = datetime.now()
            self.set_session_data(request, result['access_token'], result['refresh_token'], int(now.timestamp()) + result['expires_in'])
        except Exception as e:
            print(e)

    def _get_auth_app(self, cache=None):
        auth_app = msal.ConfidentialClientApplication(
            client_id=settings.MICROSOFT_CLIENT_ID,
            client_credential=settings.MICROSOFT_CLIENT_SECRET,
            authority="https://login.microsoftonline.com/common", ## may need to change to the tenan ID, not the common?
            token_cache=cache
        )
        return auth_app

    def get_auth_app(self, request):
        cache = self.load_cache(request)
        auth_app = self._get_auth_app(cache)
        return auth_app

    def load_cache(self, request):
        # Check for a token cache in the session
        cache = msal.SerializableTokenCache()
        if request.session.get('token_cache'):
            cache.deserialize(request.session['token_cache'])
        return cache

    def save_cache(self, request, cache):
        # If cache has changed, persist back to session
        if cache.has_state_changed:
            request.session['token_cache'] = cache.serialize()
            request.session.save()

    def get_token_from_code(self, request):
        cache = self.load_cache(request)
        auth_app = self.get_auth_app(request)

        # Get the flow saved in session
        flow = request.session.pop('auth_flow', {})
        result = auth_app.acquire_token_by_auth_code_flow(flow, request.GET)
        self.save_cache(request, cache)

        return result

    def login(self, request):
        if not request.user.is_authenticated:
            return redirect('/swirl/api-auth/login?next=/swirl/authenticators.html')
        app = self._get_auth_app()
        result = app.initiate_auth_code_flow(
            scopes=scopes,
            redirect_uri=settings.MICROSOFT_REDIRECT_URI
        )
        if result and result['auth_uri']:
            try:
                request.session['auth_flow'] = result
            except Exception as e:
                print(e)
            return HttpResponseRedirect(result['auth_uri'])

    def callback(self, request):
        result = self.get_token_from_code(request)
        user = self.get_user(result['access_token'])
        self.store_user(request, user, result)
        return HttpResponseRedirect('/swirl/')

    def update_token(self, request):
        app = self.get_auth_app(request)
        session_data = self.get_session_data(request)
        if session_data:
            result = app.acquire_token_by_refresh_token(session_data[self.refresh_token_field], scopes=scopes)
            if 'access_token' in result:
                print(result['access_token'])
                now = datetime.now()
                self.set_session_data(request, result['access_token'], result['refresh_token'], int(now.timestamp()) + result['expires_in'])
                request.session.save()
                return True
        print('redirect')
        return self.login(request)