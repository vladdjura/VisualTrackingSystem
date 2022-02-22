from credentials import account_sid, auth_token, my_cell, my_twilio 

from twilio.rest import Client

# Find these values at https://twilio.com/user/account
client = Client(account_sid, auth_token)

my_msg = "Hello!!!"

message = client.messages.create(to=my_cell, from_=my_twilio, body=my_msg)