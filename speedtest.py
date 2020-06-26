#!/usr/bin/env python3
import sys
import time
import argparse
import subprocess

parser = argparse.ArgumentParser(description='Speed test.')
parser.add_argument('-n', '--num', default=0, type=int, help='Nuber of tests')
parser.add_argument('-s', '--sec', default=10, type=int, help='Sleep seconds between test')
args = parser.parse_args()

command = [
    'speedtest',
    '-s', '15047',
    '-f', 'tsv',
    # '--output-header'
]

date_command = ['date', '+%F %T']

def print_speed():
    ret = subprocess.run(command, stdout=subprocess.PIPE)
    line = ret.stdout.decode()
    line = line.rstrip('\n')

    fields = line.split('\t')
    if len(fields) != 10:
        print('ERROR:', line, file=sys.stderr)
        sys.exit(1)

    ret = subprocess.run(date_command, stdout=subprocess.PIPE)
    date_time = ret.stdout.decode().rstrip('\n')

    server_name, server_id, latency, jitter, packet_loss, download, upload, download_bytes, upload_bytes, share_url = fields
    download_mbps = int(download) * 8 / 1000000
    upload_mbps = int(upload) * 8 / 1000000
    print(f'{date_time} {float(latency):>6.3f} ms {download_mbps:>7.2f} Mbit/s {upload_mbps:>7.2f} Mbit/s  {server_name}')

count = 0
while True:
    print_speed()
    if args.num:
        count += 1
        if count >= args.num:
            sys.exit()
    time.sleep(args.sec)
