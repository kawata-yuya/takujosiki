import requests

def send_sheet(text, secret_url):
    payload = {'text': text}
    r = requests.get(secret_url, params=payload)