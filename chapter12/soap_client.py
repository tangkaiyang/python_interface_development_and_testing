from suds.client import Client

# 使用库suds_jurko:https://bitbucket.org/jurko/suds
# web service查询:http://www.webxml.com.cn/zh_cn/web_services.aspx

# 电话号码查询归属地
url = 'http://ws.webxml.com.cn/WebServices/MobileCodeWS.asmx?wsdl'
client = Client(url)
# print(client)
result = client.service.getMobileCodeInfo(13121907110)
print(result)