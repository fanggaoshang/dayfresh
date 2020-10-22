import smtplib
from email.mime.text import MIMEText

message = MIMEText("hello, jack")
message["subject"] = "hello, are you?"

stmp = smtplib.SMTP_SSL('smtp.163.com', 994)
stmp.login("fangyingdon@163.com", "NVAWJVGUEAPPNYBW")
stmp.sendmail("fangyingdon@163.com", ["786914141@qq.com"], message.as_string())
stmp.close()