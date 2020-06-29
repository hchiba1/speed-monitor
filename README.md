# Speed monitor
A wrapper script of **Speedtest CLI** by Ookla (https://www.speedtest.net/apps/cli).

Repeat the `speedtest` command with a specified interval.

## Prerequisite
Download the Speedtest CLI and uncompress it.

The `speedtest` command should be instaled in the command path.

## Usage
```
usage: speed-monitor.py [-h] [-H] [-n NUM] [-t SEC] [-s SERVER]
                        [--ambient AMBIENT] [-l]

Repeat the Speedtest by Ookla

optional arguments:
  -h, --help            show this help message and exit
  -H, --header          output header line
  -n NUM, --num NUM     limits the number of mesurements
  -t SEC, --sec SEC     sleep between tests (in seconds)
  -s SERVER, --server SERVER
                        server ID
  --ambient AMBIENT     channel and key for Ambient
  -l, --list            list servers
```

## Usecases
### Use in default settings
Default interval is 3600 sec (1 hour)

Default server is OPEN Project (via 20G SINET) (Tokyo, Japan) (ID:15047)
```
./speed-monitor.py
```
### 3 times with no interval, output with header
```
./speed-monitor.py -n 3 --sec 0 --header
```
### List available servers
```
./speed-monitor.py -l
```
