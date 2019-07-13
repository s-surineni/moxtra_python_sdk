import base64
import hmac
import hashlib
import json
import time
import re
import requests
from uuid import uuid4


class Moxtra:
    endpoint = "https://apisandbox.moxtra.com/oauth/token"
    def __init__(self, client_id,
                 client_secret,
                 version='v1',
                 production=False):
        # self.endpoint = endpoint
        self.client_id = client_id
        self.client_secret = client_secret
        self.endpoint = "https://api.moxtra.com/" if production else "https://apisandbox.moxtra.com/"
        self.endpoint += version + '/'

    # need to provide a way to send optional parameters
    def get_access_token(self, unique_id=None, *args, **kwargs):
        # Think of other ways to implement this
        if not unique_id:
            unique_id = str(uuid4())
    
        #
        timestamp = str(int(time.time() * 1000))
        msg = self.client_id + unique_id + timestamp
        signature = base64.urlsafe_b64encode(hmac.new(key=self.client_secret, msg=msg, digestmod=hashlib.sha256).digest())
        # remove the tail "="
        signature = re.sub(r'=+$', '', signature)
    
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'http://www.moxtra.com/auth_uniqueid',
            'uniqueid': unique_id, 
            'timestamp': timestamp,
        }
        r = requests.post(self.endpoint + 'oauth/token', params = params)
        return r.json()
