import requests
import json


URL = "https://script.google.com/macros/s/AKfycbzT27Hj2osK8Z6bobU09Z6TkryOaHnQnUSWA6CLQO43RlKVVxggJwwatHVEDs6-4G08BA/exec?"

def _post(wsName, action, payload):
    headers = { 'Content-Type': 'application/json' }
    payload = json.dumps(payload)
    if action == 'add':
        url = URL + f'wsname={wsName}&action={action}'
        response = requests.request('POST', url, headers=headers, data=payload)
        return response.text

def _get(wsname, action):
    url = URL + f'wsname={wsname}&action={action}'
    try:
        response = requests.request("GET", url)
        return response.json()
    except TimeoutError as e:
        print(e)
        _get(wsname, action)