from suds.client import Client
from suds.xsd.doctor import ImportDoctor, Import

# WebService接口要求我们在调用是显式的指定调用标准

url = "http://ws.webxml.com.cn/WebServices/WeatherWS.asmx?wsdl"
imp = Import('http://www.w3.org/2001/XMLSchema',
             location="http://www.w3.org/2001/XMLSchema.xsd")
imp.filter.add('http://WebXml.com.cn/')
client = Client(url, plugins=[ImportDoctor(imp)])
print(client)
# result = client.service.getWeather('311102', 'a8d737d89a084c0698e2071af799508b')
result = client.service.getSupportCityDataset('31119')
print(result)
# print(client.service.getRegionCountry())
# print(client.service.getRegionDataset())
# print(client.service.getRegionProvince())
