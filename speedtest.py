#!/usr/bin/env python3
import sys
import argparse
import subprocess

parser = argparse.ArgumentParser(description='Speed test.')
args = parser.parse_args()

command = [
    'speedtest',
    '-s', '15047',
    '-f', 'tsv',
    # '--output-header'
]

ret = subprocess.run(command, stdout=subprocess.PIPE)
line = ret.stdout.decode()
# line = sys.stdin.readline()
line = line.rstrip('\n')
# print(line)

fields = line.split('\t')
if len(fields) != 10:
    print('ERROR:', line, file=sys.stderr)
    sys.exit(1)

date_command = ['date', '+%F %T']
ret = subprocess.run(date_command, stdout=subprocess.PIPE)
date_time = ret.stdout.decode().rstrip('\n')

server_name, server_id, latency, jitter, packet_loss, download, upload, download_bytes, upload_bytes, share_url = fields
latency_float = float(latency)
download_mbps = int(download) * 8 / 1000000
upload_mbps = int(upload) * 8 / 1000000

# output = "{0} {1:>6.3f} ms {2:>7.2f} Mbit/s {3:>7.2f} Mbit/s".format(
#     date_time, float(latency), download_mbps, upload_mbps)
# print(output)
print(f'{date_time} {latency_float:>6.3f} ms {download_mbps:>7.2f} Mbit/s {upload_mbps:>7.2f} Mbit/s  {server_name}')
