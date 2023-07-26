import datetime

import jwt

access_token_owner = jwt.encode(
        {'id': '3ba523c8-99f8-4779-b4db-416513b2bf85', 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
         'user_type': 'owner'},
        'thisissecret',
        algorithm='HS256'
    )
access_token_client = jwt.encode(
        {'id': '3b39bb85-17b5-4f4d-a963-f8f4a9b58dd4', 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
         'user_type': 'client'},
        'thisissecret',
        algorithm='HS256'
    )