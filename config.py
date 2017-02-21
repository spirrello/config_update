#!/usr/bin/python
"""
This scrip will read a file with a list of ip addresses and connect over ssh or telnet
to make the changes listed in config_commands variable.

You can use whatever you'd like in the config_commands var.  For the original intent of this Script
we had to add snmp information to prepare for a Prime Infrastructure inventory discovery.
"""

#import netmiko
from netmiko import ConnectHandler
import getpass
import argparse

#Configurations to push.
#snmp_acl = 'SNMP-MGT'
snmp_read = 'snmp-server community READONLY RO'
snmp_write = 'snmp-server community READWRITE RW'
snmp_location = 'snmp-server location LOCATION'
snmp_contact = 'snmp-server contact someone@gmail.com'
config_commands = [snmp_read,snmp_write,snmp_location,snmp_contact] 


parser = argparse.ArgumentParser(
       description='Script for pushing configuration changes.')

parser.add_argument('-c', '--conn', required=True, action='store',
                   help='Valid options are telnet or ssh.')

parser.add_argument('-o', '--os', required=True, action='store',
                   help='Identify IOS or NX-OS.')

config_args = parser.parse_args()
config_args.os = config_args.os.lower()

username = input("Please enter username: ")
password = getpass.getpass(prompt='Password: ', stream=None)

file_name = input("Please enter the file name to read: ")

#Load the file into memory as a list
f = open(file_name, 'r')
ip_list =  list(f)
f.close()


#List for devices we could not update.
failed_list = []

for ip in ip_list:
    try:
        print("\nConnecting to {0}".format(ip.rstrip()))
        #Needed logic for devices that have Telnet only vs SSH.
        if config_args.conn == 'telnet' and config_args.os == 'ios':
            net_connect = ConnectHandler(device_type='cisco_ios_telnet', ip=ip.rstrip(),username=username,password=password,timeout=5)
        if config_args.conn == 'ssh' and config_args.os == 'ios':
            net_connect = ConnectHandler(device_type='cisco_ios', ip=ip.rstrip(),username=username,password=password,timeout=5)
        if config_args.conn == 'ssh' and config_args.os == 'nxos':
            net_connect = ConnectHandler(device_type='cisco_nxos', ip=ip.rstrip(),username=username,password=password,timeout=5)
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
    print("Configuration update has completed.  These devices however failed:\n")

    for node in failed_list:
        print(node)
else:
    print("Configuration update has completed.") 

