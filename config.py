#!/usr/bin/python
"""

"""

import netmiko
from netmiko import ConnectHandler
import getpass

#Configurations to push.
#snmp_acl = 'SNMP-MGT'
snmp_read = 'snmp-server community READONLY RO'
snmp_write = 'snmp-server community READWRITE RW'
snmp_location = 'snmp-server location LOCATION'
snmp_contact = 'snmp-server contact someone@gmail.com'
config_commands = [snmp_read,snmp_write,snmp_location,snmp_contact] 

username = input("Please enter username: ")
password = getpass.getpass(prompt='Password: ', stream=None)

file_name = input("Please enter the file name to read: ")

f = open(file_name, 'r')
#f.read()

ip_list =  list(f)

f.close()

print (ip_list)
# for i in ip_list:
#     print(i.rstrip())

failed_list = []

for ip in ip_list:
    try:
        print("\nConnecting to {0}".format(ip.rstrip()))
        net_connect = ConnectHandler(device_type='cisco_ios', ip=ip.rstrip(),username=username,password=password,timeout=5)

        output = net_connect.send_config_set(config_commands)

        print("Configuration sent....\n {0}".format(output))

        output = net_connect.send_command("sh run | i snmp")

        print("Check configuration:")

        print(output)

        net_connect.disconnect()

    except Exception as e:
        failed_list.append(ip)
        print("Error with {0}\n {1}".format(ip.rstrip(),e))

if len(failed_list) > 0:
    print("Configuration update has completed.  These devices however failed:")

    for node in failed_list:
        print(node)
else:
    print("Configuration update has completed.") 
# parser = argparse.ArgumentParser(
#        description='Reads file of ip addresses and pushes configurations.')
# parser.add_argument('-f', '--file', required=False, action='store',
#                  help='Name of file to read.')
