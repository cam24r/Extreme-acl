#!/usr/bin/env python 

"""
Author: Luis Jimenez
Purpose: Parse through .pol files in a directory and convert the policies to a CSV file
"""

from ttp import ttp
import json
import os
import csv



'''
Define a template to fetch specific values from Extreme ACL config
'''

ttp_template = """
entry {{ acl_name }}{
if {
   protocol {{ protocol }} ;
   source-address {{ src_ip }} ;
   source-port {{ src_port }} ;
   destination-address {{ dst_ip }} ;
   destination-port {{ dst_port }} ;
}
 then{
    {{ action }} ;
}
}
"""

'''
Create Summary CSV file
'''

with open ('access_list_summary.csv', 'w',newline='') as output_file:
   data_writer = csv.writer(output_file, delimiter=',', quotechar='"')
   data_writer.writerow(['Name', 'Action', 'Protocol', 'Src-Address', 'Src-Port', 'Dst-Address', 'Dst-Port'])

'''
Grab Current directory
'''

path = os.getcwd()
files = os.listdir(path)

'''
read all .pol files in folder
convert json to dictionary
grab all fields from .pol files
'''

'''
Write relevant information in CSV file
'''
def writer(acl_name, action, protocol, src_add, src_prt, dst_add, dst_prt):
   with open ('access_list_summary.csv', 'a',newline='') as output_file:
      data_writer = csv.writer(output_file, delimiter=',', quotechar='"')
      data_writer.writerow([acl_name, action, protocol, src_add, src_prt, dst_add, dst_prt])

for file in files:
   if file.endswith('.pol'):
      parser = ttp(data = file , template = ttp_template )
      parser.parse()
      results = parser.result(format='json') [0]
      json_object = json.loads(results)[0]

#      print('#### ' + file + " ####")

      for key in json_object:
         acl_name = key['acl_name']
         action = 'None' if ("action" not in key.keys()) else key['action']
         protocol = 'ip' if ('protocol' not in key.keys() or (key['protocol'] == 'ipip')) else key['protocol']
         source_address = 'any' if ('src_ip' not in key.keys()) else key['src_ip']
         destination_address = "any" if ('dst_ip' not in key.keys()) else key['dst_ip']
         source_port = "any" if ('src_port' not in key.keys()) else key['src_port']
         source_port = ' ' if (protocol == "ip") else source_port
         destination_port = "any" if ('dst_port' not in key.keys()) else key['dst_port']
         destination_port = ' ' if (protocol == 'ip') else destination_port
         writer(acl_name, action, protocol, source_address, source_port, destination_address, destination_port)

#         print(acl_name + " " + action + " " + protocol + " " + source_address + " " + source_port + " " + destination_address + " " + destination_port)


