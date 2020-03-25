from twilio.rest import Client
from otp_gen import get_otp 


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
def send_otp_sms(user_phone):
 account_sid = 'ACa0b413564f3a42afaa1551c7f72f8165'
 auth_token = '826eb4d0525ac467e790f3ea3e872e87'
 client = Client(account_sid, auth_token)
 user_otp = get_otp(user_phone)
 message = client.messages.create(
         body   =  'Your OTP for Covid Help is :'+str(user_otp),
         from_  =  '+12058465187',
         to     =  str(user_phone),
     )

 print(message.sid)