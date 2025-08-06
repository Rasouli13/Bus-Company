    
from kavenegar import *
def SendOtpCode(phone_number, code):
    try:
        api = KavenegarAPI('41544E527342645475344730574D476946313359376D616E58546E494F4D70446262414A51637A483570733D')
        params = {
            'sender': '2000660110',#optional
            'receptor': phone_number,#multiple mobile number, split by comma
            'message': f'کد تایید شما {code}',
        } 
        response = api.sms_send(params)
        print(response)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)