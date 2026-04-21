import pyeapi
import json

# 1. 먼저 통신을 위한 '연결' 객체를 생성합니다.
connection = pyeapi.client.connect(
    transport='http',
    host='172.20.20.20',
    username='admin',
    password='admin'
)

# 2. 이 연결을 사용하여 'Node' 객체를 생성합니다. (여기가 핵심입니다!)
node = pyeapi.client.Node(connection)

# 3. 이제 Node 객체에서 run_commands를 호출할 수 있습니다.
try:
    response = node.run_commands(['show ip interface brief'], encoding='json')
    data = response[0]
    
    with open("./parsing/running_config.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print("설정 추출 성공!")

except Exception as e:
    print(f"에러 발생: {e}")