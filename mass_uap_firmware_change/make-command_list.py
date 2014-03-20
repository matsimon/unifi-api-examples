#!/usr/bin/env python

import argparse
from unifi.controller import Controller

parser = argparse.ArgumentParser(description='Create SSH update script for syswrapper.sh based firmware mass-upgrade.')
parser.add_argument('-c', '--controller', help='Controller DNS name or IP, this cannot be localhost here.', required=True)
parser.add_argument('-u', '--user', help='Site admin username.', required=True)
parser.add_argument('-p', '--password', help='Site admin password.', required=True)
parser.add_argument('-t', '--targetversion', help='Target firmware version. Look up precise versioning in the Ubiquiti KB, also see /usr/lib/unifi/dl/firmware/', required=True)
parser.add_argument('-a', '--apiversion', help='Base version of the AP (v2 or v3)', required=False, default='v2')
parser.add_argument('-s', '--site', help='For --apiversion v3 only, chosee site name', required=False, default='default')

args = parser.parse_args()

site_ctrl_version = args.targetversion
c = Controller(args.controller, args.user, args.password, args.apiversion, args.site)

command_list = open('command_list.sh', 'w+')

updated = 0
needs_update = 0

for ap in c.get_aps():

    if ap['version'] == site_ctrl_version:
        updated = updated + 1

    else:
        needs_update = needs_update+1

        command_list.write('sshpass -p '
                        + args.password
                        + ' ssh -F openssh.config '
                        + args.user + '@' + ap['ip']
                        + ' \"syswrapper.sh upgrade http://'
                        + args.controller
                        + ':8080/dl/firmware/' + ap['model']
                        + '/' + args.targetversion + '/firmware.bin\"\n')

print 'APs that require update:'
print needs_update
print 'APs that are up-to-date:'
print updated
print 'command_list.sh created, verify it, then chmod 755 the file and execute to update.'

command_list.close()
