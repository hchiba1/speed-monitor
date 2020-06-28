# Speed monitor
A wrapper script of **Speedtest CLI** by Ookla (https://www.speedtest.net/apps/cli).

Repeat the speedtest with a specified interval.

## Prerequisite
Download the Speedtest CLI and uncompress it.

The `speedtest` command should be instaled in the command path.

## Usage
```
usage: speed-monitor.py [-h] [-n NUM] [-s SEC] [-H] [-l] [--server SERVER]
                        [--ambient AMBIENT]

Repeat the Speedtest by Ookla

optional arguments:
  -h, --help         show this help message and exit
  -n NUM, --num NUM  limits the number of mesurements
  -s SEC, --sec SEC  sleep between tests (in seconds)
  -H, --header       output header line
  -l, --list         list servers
  --server SERVER    server ID
  --ambient AMBIENT  channel and key for Ambient
```

## Example usecase
### Use in default settings
Default interval is 3600 sec (1 hour)
Default server is OPEN Project (via 20G SINET) (Tokyo, Japan) (ID:15047)
```
./speed-monitor.py
```
### 3 times with no interval, output with header
```
./speed-monitor.py -n 3 -s 0 -H
```
### List servers
```
./speed-monitor.py -l
```
