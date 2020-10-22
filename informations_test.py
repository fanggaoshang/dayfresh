from ronglian_sms_sdk import SmsSDK

accId = "8a216da8751c49c701753e68b1110a4f"
accToken = "df298cfeb3084a1ab89b14ebcb5bdece"
appId = "8a216da8751c49c701753e68b2700a56"
sdk = SmsSDK(accId, accToken, appId)
ret = sdk.sendMessage(tid='1', mobile="17043763109", datas=('12345', '2'))
print("=========================================")
print(ret)
