from send_otp import send_otp_sms
from validate_phone import validate_phone

phone = '+917044546783'
send_otp_sms(phone)
otp =input('Enter otp')
if(validate_phone(phone,otp)):
    print("Authenticated")
else:
    print("Fake")