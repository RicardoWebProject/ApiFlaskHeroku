from requests import Response, post
from typing import List


class Mailgun():
    MAILGUN_DOMAIN = 'sandbox0f25a3c3b0b347688c5102b071de335f.mailgun.org'
    MAILGUN_API_KEY = '73e71c6131c17199bec3c80082519e53-100b5c8d-000054cf'
    FROM_TITLE = 'Stores REST API'  #Nombre de quién envía
    FROM_EMAIL = 'postmaster@sandbox0f25a3c3b0b347688c5102b071de335f.mailgun.org'
    
    @classmethod
    def send_email(cls, email: List[str], subject: str, text: str, html: str) -> Response:
        return post(
            f'https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages',
            auth=('api', cls.MAILGUN_API_KEY),
            data={
                'from': f'{cls.FROM_TITLE} <{cls.FROM_EMAIL}>',
                'to': email,
                'subject': subject,
                'text': text,
                'html': html
            }
        )