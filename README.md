# Network Automation Project

## Overview
기존의 CLI 기반의 네트워크 장비 설정 및 검증은 시간이 많이 소모되고, 사람의 실수가 발생할 수 있다.

해당 프로젝트는 Ansible을 이용해서 Arista cEOS 장비의 설정을 자동화 하고, pyeapi를 이용해서 장비의 상태를 수집한다.

수집된 데이터에서 필요한 내용만 필터링해서 report.json으로 저장되며, 이를 통해서 각 장비의 상태를 한 번에 확인할 수 있다.

## Purpose
- 반복적인 작업 감소
- 일관된 네트워크 구성 보장
- 장비에 직접 접속하지 않고 상태 확인 가능

## Tech Stack
* Ansible
* Containerlab
* Arista cEOS
* pyeapi

## Topology
![topology](./img/topo.png)

## Features
- ansible 네트워크 자동화
    - api 활성화
    - IP address 설정
    - Loopback 설정
    - OSPF 설정

- pyeapi를 이용한 데이터 수집
    - interface와 OSPF 정보 추출

- json 기반 데이터 구조화
    - 필요한 데이터만 필터링해서 json으로 저장


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

---

## What I Learned
- containerlab을 이용해서 가상 네트워크를 구성하는 방법을 배웠다.
- Ansible을 이용해서 각 장비에 접근해서 자동으로 설정을 밀어 넣는 방법을 배웠다.
- host_vars와 group_vars를 이용해서 각 장비 마다 설정해야 할 내용을 분리하는 방법을 배웠다.
- roles을 이용해서 각 기능을 분리해서 재사용성을 높이는 방법을 배웠다.
- pyeapi를 이용해서 각 장비의 현재 상태를 json으로 수집하고 필요한 데이터만 필터링 하는 방법을 배웠다.