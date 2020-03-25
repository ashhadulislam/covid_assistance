def get_otp(number):
    enc = {"0":"8","1":"4","2":"5","3":"2","4":"6","5":"3",
           "6":"0","7":"9","8":"1","9":"7"}
    number = str(number)
    otp = enc[number[1]]+enc[number[7]]+enc[number[2]]+enc[number[6]]+enc[number[4]]
    return otp