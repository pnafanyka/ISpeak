import os
import requests
import uuid
import time

from read_certs import CA_BUNDLE

AUTH_URL = os.getenv('AUTH_URL')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')

class Auth():

    def __init__(self):
        api_token, token_expiration_timestamp = self.get_auth_token()
        self.api_token = api_token
        self.token_expiration_timestamp = token_expiration_timestamp


    def get_auth_token(self):
        payload = 'scope=GIGACHAT_API_PERS'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': f'{str(uuid.uuid4())}',
        'Authorization': f'Bearer {AUTH_TOKEN}'
        }

        response = requests.request("POST", url=AUTH_URL, headers=headers, data=payload, verify=CA_BUNDLE)

        if response.status_code == 200:
            content = response.json()
            return content['access_token'], content['expires_at']
        else:
            print('Не прошли аутентификацию')
            raise KeyError

    def is_expired(self, margin_ms: int = 60_000) -> bool:
        """True, если токена нет или он истекает в течение margin_ms (по умолчанию минута)."""
        return time.time() * 1000 >= self.token_expiration_timestamp - margin_ms
        
        
    def update(self):
        self.api_token, self.token_expiration_timestamp = self.get_auth_token()


authenticator = Auth()

if __name__=='__main__':
    print(authenticator.api_token)

