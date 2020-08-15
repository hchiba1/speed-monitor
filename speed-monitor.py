#!/usr/bin/env python3
import sys
import io
import re
import json
import time
import argparse
import subprocess
import requests
import xml.etree.ElementTree as ET

def unbuffered_text_io(stream):
    if (not isinstance(stream, io.TextIOWrapper) or not hasattr(stream, 'buffer')):
        return stream
    raw = stream.buffer
    if isinstance(raw, io.BufferedIOBase) and hasattr(raw, 'raw'):
        raw = raw.raw
    return io.TextIOWrapper(raw, encoding=stream.encoding, errors=stream.errors, write_through=True)
sys.stdout = unbuffered_text_io(sys.stdout)
sys.stderr = unbuffered_text_io(sys.stderr)

parser = argparse.ArgumentParser(description='Repeat the Speedtest by Ookla')
parser.add_argument('-H', '--header', action='store_true', help='output header line')
parser.add_argument('-n', '--num', default=0, type=int, help='limits the number of mesurements')
parser.add_argument('-t', '--sec', default=3600, type=int, help='sleep between tests (in seconds)')
parser.add_argument('-s', '--server', nargs='+', default=[15047], help='server ID')
parser.add_argument('--ambient', help='channel and key for Ambient')
parser.add_argument('-l', '--list', action='store_true', help='list servers')
args = parser.parse_args()

date_command = ['date', '+%F %T']

def main():
    channel, key = '', ''
    if args.ambient:
        matched = re.search(r'^(\d+):([0-9a-z]+)$', args.ambient)
        if not matched:
            print('ERROR: invalid value in --ambient')
            sys.exit(1)
        channel, key = matched.groups()

    if args.list:
        print_servers()
        return

    if args.header:
        print('{0:} {1:9} {2:14} {3:14} {4:9} {5:9} {6:4} {7:9} {8}'.format(
            'Date       Time    ', '  Ping', '  Download', '  Upload', ' Download', '  Upload', ' Loss', '  Jitter', 'Server'), flush=True)

    repeat_speed_test(args.server, channel, key)

def print_servers():
    res = requests.get('http://c.speedtest.net/speedtest-servers-static.php')
    # res = requests.get('http://c.speedtest.net/speedtest-servers.php')
    # res = requests.get('http://www.speedtest.net/speedtest-servers-static.php')
    # res = requests.get('http://www.speedtest.net/speedtest-servers.php')
    if res.status_code == requests.codes.ok:
        settings = ET.fromstring(res.text)
        for servers in settings:
            for server in servers:
                print(f'{server.attrib["id"]:5}',
                      f'({server.attrib["lat"]},{server.attrib["lon"]})',
                      f'{server.attrib["country"]} ({server.attrib["name"]}) {server.attrib["sponsor"]}',
                      sep=' ')

def print_speed(server, channel, key):
    ret = subprocess.run(date_command, stdout=subprocess.PIPE)
    date_time = ret.stdout.decode().rstrip('\n')

    command = [ 'speedtest', '-s', str(server), '-f', 'json' ]
    ret = subprocess.run(command, stdout=subprocess.PIPE, timeout=300)
    if ret.returncode != 0:
        print(f'ERROR: speedtest server={server} retcode={ret.returncode}', flush=True)
        sys.exit(ret.returncode)
    # line = ret.stdout.decode()
    # line = line.rstrip('\n')
    # fields = line.split('\t')
    # if len(fields) != 10:
    #     print('ERROR:', line, file=sys.stderr)
    #     return
    # server_name, server_id, latency, jitter, packet_loss, download, upload, download_bytes, upload_bytes, share_url = fields
    out = ret.stdout.decode()
    jsonData = json.loads(out)
    server_name = jsonData['server']['name']
    server_location = jsonData['server']['location']
    server_country = jsonData['server']['country']
    server_id = jsonData['server']['id']
    latency = jsonData['ping']['latency']
    jitter = jsonData['ping']['jitter']
    packet_loss= jsonData.get('packetLoss', 'N/A')
    download = jsonData['download']['bandwidth']
    download_bytes = jsonData['download']['bytes']
    upload = jsonData['upload']['bandwidth']
    upload_bytes = jsonData['upload']['bytes']

    ping = f'{float(latency):.2f}'
    download_mbps = int(download) * 8 / 1000000
    upload_mbps = int(upload) * 8 / 1000000
    download_mb = int(download_bytes) / 1000000
    upload_mb = int(upload_bytes) / 1000000
    if packet_loss == 'N/A':
        packet_loss = f'{packet_loss:>5}'
    else:
        packet_loss = f'{float(packet_loss):>4.1f}%'
    print(f'{date_time} {ping:>6} ms',
          f'{download_mbps:>7.2f} Mbit/s {upload_mbps:>7.2f} Mbit/s',
          f'{download_mb:>6.1f} MB {upload_mb:>6.1f} MB',
          f'{packet_loss} {float(jitter):>6.2f} ms',
          # f'{server_id:5} {server_location} ({server_country})',
          f'{server_id:5} {server_country} ({server_location})',
          f'{server_name}',
          flush=True)

    if args.ambient:
        data = [{'created': date_time, 'd1': download_mbps, 'd2': upload_mbps, 'd3': ping}]
        res = requests.post(f'https://ambidata.io/api/v2/channels/{channel}/dataarray', json={'writeKey': key, 'data': data})
        if res.status_code != requests.codes.ok:
            print('ERROR:', res.status_code, file=sys.stderr, flush=True)

def repeat_speed_test(servers, channel, key):
    count = 0
    while True:
        for server in servers:
            try:
                print_speed(server, channel, key)
            except Exception as e:
                print(f'ERROR: speedtest server={server}', flush=True)
                print(e, file=sys.stderr, flush=True)
        if args.num:
            count += 1
            if count >= args.num:
                return
        time.sleep(args.sec)

try:
    main()
except KeyboardInterrupt:
    print('', file=sys.stderr)
except BrokenPipeError:
    pass
