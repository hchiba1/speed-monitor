#!/usr/bin/env python3
import sys
import time
import argparse
import subprocess

parser = argparse.ArgumentParser(description='Repeat the Speedtest by Ookla')
parser.add_argument('-n', '--num', default=0, type=int, help='limits the number of mesurements')
parser.add_argument('-s', '--sec', default=0, type=int, help='sleep between tests (in seconds)')
parser.add_argument('--server', default='15047', help='server ID')
args = parser.parse_args()

command = [
    'speedtest',
    '-s', args.server,
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
    download_mb = int(download_bytes) / 1000000
    upload_mb = int(upload_bytes) / 1000000
    print(f'{date_time} {float(latency):>6.2f} ms',
          f'{download_mbps:>7.2f} Mbit/s {upload_mbps:>7.2f} Mbit/s',
          f'{download_mb:>6.1f} MB {upload_mb:>6.1f} MB',
          f'{float(packet_loss):>4.1f}% {float(jitter):>6.2f} ms  {server_name}')

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
