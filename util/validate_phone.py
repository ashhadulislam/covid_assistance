from otp_gen import get_otp 

def validate_phone(user_phone,user_otp):
    correct_otp = get_otp(user_phone)
    user_otp = str(user_otp)
    if(user_otp == correct_otp):
         return True
    return False


