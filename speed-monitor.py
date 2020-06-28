#!/usr/bin/env python3
import sys
import re
import time
import argparse
import subprocess
import requests

parser = argparse.ArgumentParser(description='Repeat the Speedtest by Ookla')
parser.add_argument('-n', '--num', default=0, type=int, help='limits the number of mesurements')
parser.add_argument('-s', '--sec', default=3600, type=int, help='sleep between tests (in seconds)')
parser.add_argument('-H', '--header', action='store_true', help='output header line')
parser.add_argument('--server', default='15047', help='server ID')
parser.add_argument('--ambient', help='channel and key for Ambient service')
args = parser.parse_args()

command = [
    'speedtest',
    '-s', args.server,
    '-f', 'tsv',
    # '--output-header'
]

date_command = ['date', '+%F %T']

channel, key = '', ''
if args.ambient:
    matched = re.search(r'^(\d+):([0-9a-z]+)$', args.ambient)
    if not matched:
        print('ERROR: invalid valud in --ambient')
        sys.exit(1)
    channel, key = matched.groups()

def print_speed():
    ret = subprocess.run(command, stdout=subprocess.PIPE)
    line = ret.stdout.decode()
    line = line.rstrip('\n')

    fields = line.split('\t')
    if len(fields) != 10:
        print('ERROR:', line, file=sys.stderr)
        return

    ret = subprocess.run(date_command, stdout=subprocess.PIPE)
    date_time = ret.stdout.decode().rstrip('\n')

    server_name, server_id, latency, jitter, packet_loss, download, upload, download_bytes, upload_bytes, share_url = fields
    ping = f'{float(latency):.2f}'
    download_mbps = int(download) * 8 / 1000000
    upload_mbps = int(upload) * 8 / 1000000
    download_mb = int(download_bytes) / 1000000
    upload_mb = int(upload_bytes) / 1000000
    print(f'{date_time} {ping:>6} ms',
          f'{download_mbps:>7.2f} Mbit/s {upload_mbps:>7.2f} Mbit/s',
          f'{download_mb:>6.1f} MB {upload_mb:>6.1f} MB',
          f'{float(packet_loss):>4.1f}% {float(jitter):>6.2f} ms  {server_name}')

    if args.ambient:
        data = [{'created': date_time, 'd1': download_mbps, 'd2': upload_mbps, 'd3': ping}]
        res = requests.post(f'http://ambidata.io/api/v2/channels/{channel}/dataarray', json={'writeKey': key, 'data': data})
        if res.status_code != requests.codes.ok:
            print('ERROR:', res.status_code, file=sys.stderr)

def repeat_speed_test():
    count = 0
    while True:
        print_speed()
        if args.num:
            count += 1
            if count >= args.num:
                return
        time.sleep(args.sec)

if args.header:
    print('{0:} {1:9} {2:14} {3:14} {4:9} {5:9} {6:4} {7:9}  {8}'.format(
        'Date       Time    ', '  Ping', '  Download', '  Upload', ' Download', '  Upload', ' Loss', '  Jitter', 'Server name'))

try:
    repeat_speed_test()
except KeyboardInterrupt:
    print('Interrupted.', file=sys.stderr)
