import requests
headers = {'User-Agent': 'Mozilla/5.0'}
payload = {'password':123,'user_id':2}

session = requests.Session()
r = session.post('http://localhost:5000/stoper', headers = headers, data = payload)
print(r)

