import requests

def send_sheet(text, title, secret_url):
    payload = {
        'text': text,
        'title': title,
    }

    r = requests.get(secret_url, params=payload)