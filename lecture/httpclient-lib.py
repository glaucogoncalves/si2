import requests

url = "http://www.google.com.br:80"

r1 = requests.get(url)

print(r1.status_code, r1.reason)
print(r1.headers)