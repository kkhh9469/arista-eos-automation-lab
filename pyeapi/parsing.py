import pyeapi
import json
from pprint import pprint
import csv


def parsing(host_ip):
    connection = pyeapi.client.connect(
        transport='http',
        host=host_ip,
        # host='172.20.20.10',
        username='admin',
        password='admin'
    )

    node = pyeapi.client.Node(connection)

    cmds = ['show ip interface brief', 'show hostname', 'sh ip ospf neighbor']

    raw_data = node.run_commands(cmds, encoding='json')

    int_info = raw_data[0]['interfaces']
    hostname = raw_data[1]['hostname']
    ospf_neighbor = raw_data[2]['vrfs']['default']['instList']
    ospf_instance_number = ospf_neighbor.keys()
    pprint(ospf_neighbor)

    data_list = []
    for int_name, details in int_info.items():
        ipv4_data = details['interfaceAddress']['ipAddr']
        ipv4_addr = ipv4_data['address']
        ipv4_mask = ipv4_data['maskLen']
        ipv4_merge = f'{ipv4_addr}/{ipv4_mask}'
        status = details['lineProtocolStatus']

        row = [hostname, int_name, status, ipv4_merge, ospf_instance_number]

        data_list.append(row)
    
    return data_list

def save_csv(data_list):
    with open('./pyeapi/report', 'w',encoding='utf-8') as f:
        writer = csv.writer(f)



# device mgmt ip list
host_ips = ['172.20.20.10', '172.20.20.20', '172.20.20.30', '172.20.20.40']
merge_data = []

for host_ip in host_ips:
    expoet_list = parsing(host_ip)
    merge_data.extend(expoet_list)

pprint(merge_data)