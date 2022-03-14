from send_otp import send_otp_sms
from validate_phone import validate_phone

phone = '+918777061118'
send_otp_sms(phone)
otp =input('Enter otp :\n')
if(validate_phone(phone,otp)):
    print("Authenticated")
else:
    print("Fake")