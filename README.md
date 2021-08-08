# Speed monitor
A wrapper script of **Speedtest CLI** by Ookla (https://www.speedtest.net/apps/cli).

Repeat the `speedtest` command with a specified interval.

## Usage
```
./speed-monitor.py
```
* Default interval is 3600 sec (1 hour)

* Default server is OPEN Project (via 20G SINET) (Tokyo, Japan) (ID:15047)

### 3 times, 0 sec interval, with header
```
./speed-monitor.py -n 3 -t 0 -H
```
### List available servers
```
./speed-monitor.py -l
```
### Help
```
./speed-monitor.py -h
```

## Installation
Download the Speedtest CLI from Ookla (https://www.speedtest.net/apps/cli) and uncompress it.

The `speedtest` command should be instaled in the command path.

Python3 `requests` module is required.
```
$ sudo pip3 install requests
```
