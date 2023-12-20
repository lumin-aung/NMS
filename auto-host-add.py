import requests
import json
import csv
 
# Zabbix API URL
zabbix_url = 'https://nms.agbisp.net/api_jsonrpc.php'
 
# Zabbix API credentials
zabbix_user = 'API'
zabbix_password = 'P@ssw0rd@12345'
 
# CSV file path
csv_file_path = 'Sample.csv'
 
# Zabbix API authentication
auth_payload = {
    'jsonrpc': '2.0',
    'method': 'user.login',
    'params': {
        'user': zabbix_user,
        'password': zabbix_password,
    },
    'id': 1,
}
 
auth_response = requests.post(zabbix_url, data=json.dumps(auth_payload), headers={'Content-Type': 'application/json'})
auth_result = auth_response.json()
 
if 'result' in auth_result:
    auth_token = auth_result['result']
 
    # Read hosts from CSV file
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            host_name = row['Hostname']
            host_ip = row['IP Address']
 
            # Add host
            host_payload = {
                'jsonrpc': '2.0',
                'method': 'host.create',
                'params': {
                    'host': host_name,
                    'interfaces': [
                        {
                            'type': 1,  # 1 for agent, 2 for SNMP
                            'main': 1,
                            'useip': 1,
                            'ip': host_ip,
                            'dns': '',
                            'port': '10050',
                        }
                    ],
                    'groups': [{'groupid': '1'}],  # Assuming '1' is the ID of the group you want to add the host to
                    'templates': [{'templateid': '10598'}]
                },
                'auth': auth_token,
                'id': 1,
            }
 
            host_response = requests.post(zabbix_url, data=json.dumps(host_payload), headers={'Content-Type': 'application/json'})
            host_result = host_response.json()
 
            if 'result' in host_result:
                print(f"Host '{host_name}' added successfully with hostid: {host_result['result']['hostids'][0]}")
            else:
                print(f"Failed to add host '{host_name}': {host_result['error']['data']}")
else:
    print(f"Authentication failed: {auth_result['error']['data']}")
