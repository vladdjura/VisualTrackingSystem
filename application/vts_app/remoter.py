import requests
from credentials import stoper_url, data_url, admin_password

def data(data_url, admin_password):
    url = data_url
    data = {'password':admin_password}
    r = requests.post(url, data = data)
    return r.json()

def stoper(stoper_url, admin_password, id):
    url = stoper_url
    data = {'password':admin_password, 'user_id': id}
    r = requests.post(url, data = data)
    return r.json()

if __name__ == '__main__':
    id=1
    #print(data(data_url, admin_password))
    print(stoper(stoper_url, admin_password, id))
