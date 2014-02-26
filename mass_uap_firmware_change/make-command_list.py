#!/usr/bin/env python

# Copyright (c)2013 Gymnasium Köniz-Lerbermatt
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

import argparse
from unifi.controller import Controller

parser = argparse.ArgumentParser(description='Create SSH update script for syswrapper.sh based firmware mass-upgrade.')
parser.add_argument('-c', '--controller', help='Controller DNS name or IP, this is not localhost here.', required=True)
parser.add_argument('-u', '--user', help='Site admin username.', required=True)
parser.add_argument('-p', '--password', help='Site admin password.', required=True)
parser.add_argument('-t', '--targetversion', help='Target firmware version.', required=True)

args = parser.parse_args()

site_ctrl = args.controller
# site_siteid = args.siteid
site_admin = args.user
site_pass = args.password
site_ctrl_version = args.targetversion

c = Controller(site_ctrl,site_admin,site_pass)

command_list = open('command_list.sh', 'w+')

updated = 0
needs_update = 0

for ap in c.get_aps():

    if ap['version'] == site_ctrl_version:
        updated=updated+1

    else:
        needs_update=needs_update+1

        command_list.write('sshpass -p ' 
                    + site_pass
                    + ' ssh -F openssh.config '
                    + site_admin + '@' + ap['ip']
                    + ' \"syswrapper.sh upgrade http://'
                    + site_ctrl
                    +':8080/dl/firmware/' + ap['model']
                     + '/' + site_ctrl_version + '/firmware.bin\"\n')

print 'APs that require update:' 
print needs_update
print 'APs that are up-to-date:'
print updated
print 'command_list.sh created, verify it, then chmod 755 the file and execute to update.'

command_list.close()
