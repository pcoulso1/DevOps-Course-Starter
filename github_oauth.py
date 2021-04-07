# Import dependnecies
import os
from oauthlib.oauth2 import WebApplicationClient
import json
import requests

# Appliction imports
from config import Config
class GithubOauthProvider:

    def __init__(self):
        self.client = WebApplicationClient(Config().GITHUB_CLIENT_ID)
        self.state = 'DevOpsUser'

    def get_client_secret(self):
        """
        Returns the client secret to be used by app for Oauth
    
        Returns:
            String: client secret
        """
        return Config.GITHUB_CLIENT_SECRET

    def get_authenticate_uri(self):
        """
        Returns the uri for the application to autehticate agaisnt
    
        Returns:
            String: the encoded uri
        """
        return self.client.prepare_request_uri('https://github.com/login/oauth/authorize', 
            redirect_uri=Config().GITHUB_LOGON_REDIRECT, 
            state=self.state)

    def get_user_info(self, authorization_response, redirect_url, code):
        """
        Makes a request to github to with the given authorization code
        to obtain a token which can then be used to retrive user information

        Args:
            authorization_response: The full redirection URL string, i.e.
                the location to which the user was redirected after successfull
                authorization.
            
            redirect_url: The redirect_url supplied with the authorization request.

            code: authorization code from github
    
        Returns:
            json: A json string containing the user information from GitHub
        """

        # Modify the protocol if OAUTHLIB_INSECURE_TRANSPORT is not set to https
        # as we are running in a container and binding to http, but GITHUG uses the 
        # external heroku URL which is TLS protected
        OAUTHLIB_INSECURE_TRANSPORT = os.getenv('OAUTHLIB_INSECURE_TRANSPORT')
        if (not OAUTHLIB_INSECURE_TRANSPORT) or OAUTHLIB_INSECURE_TRANSPORT == '0':
            authorization_response = authorization_response.replace('http://', 'https://')
            redirect_url = redirect_url.replace('http://', 'https://')

        token_url, headers, body = self.client.prepare_token_request(
            'https://github.com/login/oauth/access_token',
            authorization_response=authorization_response,
            redirect_url=redirect_url,
            code=code
        )
        
        headers["Accept"] = "application/json"

        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(Config().GITHUB_CLIENT_ID, Config().GITHUB_CLIENT_SECRET),
        )

        self.client.parse_request_body_response(token_response.text)

        uri, headers, body = self.client.add_token('https://api.github.com/user')
        userinfo_response = requests.get(uri, headers=headers, data=body)

        return userinfo_response.json()