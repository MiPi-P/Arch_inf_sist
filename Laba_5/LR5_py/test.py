import requests

data = {
    'left_time': 0,
    'right_time': 0,
    'forward_time': 1
}

response = requests.post(
    'http://192.168.1.101:8080/commands', # 'http://localhost:8080/commands', # 'http://192.168.1.100:8080/commands'
    json=data
)

print(response.text)