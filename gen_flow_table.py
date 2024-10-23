import json
import random

def generate_mac():
    return ':'.join(['{:02x}'.format(random.randint(0, 255)) for _ in range(6)])

def generate_json():
    table_entries = []
    multicast_group_entries = []

    for i in range(1, 101):  # 生成100项
        table_entry = {
            "table": "goose_table",
            "match": {
                "hdr.ethernet.dstAddr": [generate_mac(), "ff:ff:ff:ff:ff:ff"],
                "hdr.ethernet.srcAddr": [generate_mac(), "ff:ff:ff:ff:ff:ff"],
                "hdr.vlan.vid": 100,
                "hdr.goose.goose_appid": 1
            },
            "action": "goose_multicast",
            "mcast_group_id": i
        }
        table_entries.append(table_entry)

        multicast_group_entry = {
            "multicast_group_id": i,
            "replicas": [
                {"egress_port": port, "instance": 1}
                for port in range(1, 5)
            ]
        }
        multicast_group_entries.append(multicast_group_entry)

    return {
        "table_entries": table_entries,
        "multicast_group_entries": multicast_group_entries
    }

# 生成JSON
json_data = generate_json()

# 将生成的JSON写入文件
with open('generated_entries.json', 'w') as f:
    json.dump(json_data, f, indent=2)

print("已生成包含100个table_entries和100个multicast_group_entries的JSON，并保存到 generated_entries.json 文件中。")