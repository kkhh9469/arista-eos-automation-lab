# Network Automation Project

## Overview
Ansible을 이용해서 각 EOS 장비의 설정을 자동으로 변경할 수 있다.

기존에 CLI를 이용하는 것 보다 빠르게 설정을 완료 할 수 있다.

항상 동일한 결과물을 얻을 수 있으며, 설정 값만 변경하면 동일한 구성의 다른 장비에도 적용할 수 있다. 

pyeapi을 이용해서 현재 장비 설정 상태를 report.json으로 추출해서 확인할 수 있다.

각 장비에 직접 들어가서 확인할 필요 없이 report.json을 통해서 다수의 장비의 설정을 확인할 수 있다.

## Tech Stack
* Ansible
* Containerlab
* Arista cEOS
* pyeapi

## Topology
![topology](./img/topo.png)

## Features
* ansible을 이용한 자동화
    - enable API
    - config IP Address
    - config Loopback
    - config OSPF

* pyeapi를 이용한 각 장비 정보 수집 및 json으로 추출
    - parsing.py


## Example Output
report.json
```json
{
    "hostname": "spine1",
    "interfaces": [
        {
            "name": "Ethernet1",
            "status": "connected",
            "protocol": "up",
            "ip": "10.0.0.1",
            "prefix": 30,
            "network": "10.0.0.1/30"
        },
        {
            "name": "Ethernet2",
            "status": "connected",
            "protocol": "up",
            "ip": "10.0.0.5",
            "prefix": 30,
            "network": "10.0.0.5/30"
        },
        {
            "name": "Loopback0",
            "status": "connected",
            "protocol": "up",
            "ip": "1.1.1.1",
            "prefix": 32,
            "network": "1.1.1.1/32"
        },
        {
            "name": "Management0",
            "status": "connected",
            "protocol": "up",
            "ip": "172.20.20.10",
            "prefix": 24,
            "network": "172.20.20.10/24"
        }
    ],
    "ospf": [
        {
            "process_id": "1",
            "adjacency": "full",
            "area": "0.0.0.0",
            "interface": "Ethernet1",
            "neighbor_ip": "10.0.0.2"
        },
        {
            "process_id": "1",
            "adjacency": "full",
            "area": "0.0.0.0",
            "interface": "Ethernet2",
            "neighbor_ip": "10.0.0.6"
        }
    ]
}
```

---

## How to Run
Run containerlab
```bash
containerlab deploy -t containerlab/topo.yml
```

Run Ansible
```bash
ansible-playbook -i ansible/inventory/hosts.yml ansible/playbook/control.yml
```

Run Parsing
```bash
python3 pyeapi/parsing.py
```

## What I Learned
containerlab을 이용해서 가상 네트워크를 구성하는 방법을 배웠다.

ansible을 이용해서 각 장비에 접근해서 자동으로 설정을 밀어 넣는 방법을 배웠다.

host_vars와 group_vars를 이용해서 각 장비 마다 설정해야 할 내용을 분리하는 방법을 배웠다.

roles을 이용해서 코드의 재사용성은 높이는 방법을 배웠다.

pyeapi를 이용해서 각 장비의 현재 설정을 json으로 추출하고 필요한 데이터만 필터링 하는 방법을 배웠다.