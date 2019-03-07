import requests

# 查询发布会接口
url = "http://127.0.0.1:8000/api/get_event_list/"
r = requests.get(url, params={'eid': '1'})
result = r.json()
print(result)
assert result['status'] == 200
assert result['message'] == "success"
assert result['data']['name'] == "OKC vs PHI"
assert result['data']['limit'] == 20000
assert result['data']['status'] == True
assert result['data']['address'] == "切萨皮克能源球馆"
assert result['data']['start_time'] == "2019-03-01T06:18:31Z"
