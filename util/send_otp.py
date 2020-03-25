from twilio.rest import Client
from os import environ
from otp_gen import get_otp 


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
def send_otp_sms(user_phone):
 account_sid = environ.get('account_sid')
 auth_token =  environ.get('auth_token')
 client = Client(account_sid, auth_token)
 user_otp = get_otp(user_phone)
 message = client.messages.create(
         body   =  'Your OTP for Covid Help is :'+str(user_otp),
         from_  =  environ.get('reg_phone'),
         to     =  str(user_phone),
     )

 print(message.sid)