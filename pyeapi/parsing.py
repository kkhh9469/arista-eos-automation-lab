import pyeapi
from pprint import pprint
import json


# device mgmt ip list
host_ips = ['172.20.20.10', '172.20.20.20', '172.20.20.30', '172.20.20.40']
merge_data = {}

for host_ip in host_ips:
    connection = pyeapi.client.connect(
        transport='http',
        host= host_ip,
        username='admin',
        password='admin'
    )
    
    node = pyeapi.client.Node(connection)

    cmds = ['sh hostname', 'sh ip interface brief', 'sh ip ospf neighbor', 'sh ip route']
    raw_data = node.enable(cmds)
    
    hostname = raw_data[0]['result']['hostname']
    ip_info = raw_data[1]['result']['interfaces']
    ospf_info = raw_data[2]['result']['vrfs']['default']['instList']

    merge_data.setdefault(hostname, {
        "hostname": hostname,
        "interfaces": [],
        "ospf": []
    })

    for int_name, data in ip_info.items():
        name = data.get('name')
        ip = data.get('interfaceAddress').get('ipAddr').get('address')
        prefix = data.get('interfaceAddress').get('ipAddr').get('maskLen')
        int_status = data.get('interfaceStatus')
        int_protocol_status = data.get('lineProtocolStatus')

        merge_data[hostname]['interfaces'].append({
            "name": name,
            "status": int_status,
            "protocol": int_protocol_status,
            "ip": ip,
            "prefix": prefix,
            "network": f'{ip}/{prefix}'
        })

    for instant, data in ospf_info.items():
        for detail in data['ospfNeighborEntries']:
            adjacency = detail.get('adjacencyState')
            area = detail.get('details').get('areaId')
            int_addr = detail.get('interfaceAddress')
            neighboer_int = detail.get('interfaceName')

            merge_data[hostname]["ospf"].append({
                "process_id": instant,
                "adjacency": adjacency,
                "area": area,
                "interface": neighboer_int,
                "neighbor_ip": int_addr,
            })

merge_data = list(merge_data.values())

with open('./pyeapi/report.json', 'w') as f:
    json.dump(merge_data, f, indent=4)

