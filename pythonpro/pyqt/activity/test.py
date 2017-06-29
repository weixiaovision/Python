import requests


response = requests.get('http://10.10.4.180:6692/agent/testCommand?params=0001$coin 30')
print(response.text)
