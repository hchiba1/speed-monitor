#!/usr/bin/env python3
import sys
import time
import argparse
import subprocess

parser = argparse.ArgumentParser(description='Speed test.')
parser.add_argument('-n', '--num', default=0, type=int, help='Nuber of times')
parser.add_argument('-s', '--sec', default=0, type=int, help='Sleep between test')
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
        return

    ret = subprocess.run(date_command, stdout=subprocess.PIPE)
    date_time = ret.stdout.decode().rstrip('\n')

    server_name, server_id, latency, jitter, packet_loss, download, upload, download_bytes, upload_bytes, share_url = fields
    download_mbps = int(download) * 8 / 1000000
    upload_mbps = int(upload) * 8 / 1000000
    download_mb = int(download_bytes) / 1024 / 1024
    upload_mb = int(upload_bytes) / 1024 / 1024
    print(f'{date_time} {float(latency):>6.3f} ms {download_mbps:>7.2f} Mbit/s {upload_mbps:>7.2f} Mbit/s {download_mb:>5.1f} MB {upload_mb:>5.1f} MB  {server_name}')

def repeat_speed_test():
    count = 0
    while True:
        print_speed()
        if args.num:
            count += 1
            if count >= args.num:
                return
        time.sleep(args.sec)

try:
    repeat_speed_test()
except KeyboardInterrupt:
    print('Interrupted.', file=sys.stderr)
