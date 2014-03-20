#!/usr/bin/env python

import argparse
from unifi.controller import Controller

parser = argparse.ArgumentParser(description='Backup a UniFi controller site to file. WARNING: Puts significant load on your controller.')
parser.add_argument('-c', '--controller', help='Controller DNS name or IP, this is not localhost here. (default: localhost)', required=False, default='localhost')
parser.add_argument('-u', '--user', help='Site admin username.', required=True)
parser.add_argument('-p', '--password', help='Site admin password.', required=True)
parser.add_argument('-a', '--apiversion', help='Base version of the AP (v2 or v3, default: v2)', required=False, default='v2')
parser.add_argument('-s', '--site', help='For --apiversion v3 only, chosee site name (default: default)', required=False, default='default')
parser.add_argument('-f', '--file', help='Filename for backup, .unf as recommended ending (default: unifi-backup.unf):', required=False, default='unifi-backup.unf')

args = parser.parse_args()

c = Controller(args.controller, args.user, args.password, args.apiversion)
c.get_backup(args.file)
