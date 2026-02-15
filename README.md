# Daikin Legacy CLI (BRP069B41)

Asynchronous Python CLI and library for controlling legacy Daikin BRP069B41 Wi-Fi adapters using a "Golden Engine" state-persistence logic.

## Technical Requirements
* **Python 3.7+**
* **Dependencies**: `pip install aiohttp`
* **Permissions**: `chmod +x daikin_cli.py`

## Configuration
Create a `daikin.conf` file in the script directory:
```ini
IP_ADDRESS=192.168.x.x
MY_UUID=your_32_character_uuid

you must authorize the UUID with the unit once via terminal:
curl -k -H "X-Daikin-uuid: YOUR_UUID" "https://YOUR_IP/common/set_remote_regy_if?key=YOUR_KEY"


CLI Usage
Status: ./daikin_cli.py status

Power: ./daikin_cli.py on | ./daikin_cli.py force-off

Modes: ./daikin_cli.py [cool|heat|fan|dry] [temp]

Fan: ./daikin_cli.py speed [auto|eco|1-5]

Swing: ./daikin_cli.py dir [off|vertical|horizontal|3d]

Files in this Repo
daikin_cli.py: The user interface and command processor.

daikin_legacy.py: The core library handling "Golden Engine" logic (fetching state before writing).

daikin.conf: (User Created) Stores local network credentials.

daikin_readme: Technical documentation.

Example of help contents:
./daikin_cli.py
usage: daikin_cli [-h] {status,on,off,force-off,speed,dir,cool,heat,dry,fan} ...

CLI for Daikin BRP069B41 matching official app terminology.

positional arguments:
  {status,on,off,force-off,speed,dir,cool,heat,dry,fan}
                        Available Commands
    status              Show all current settings
    on                  Power ON
    off                 Power OFF (Standard)
    force-off           Attempt shutdown with verification and retries
    speed               Set Fan Speed
    dir                 Set Airflow Swing
    cool                Set to COOL mode
    heat                Set to HEAT mode
    dry                 Set to DRY mode
    fan                 Set to FAN mode

options:
  -h, --help            show this help message and exit

EXAMPLES:
  Set Fan Speed:        ./daikin_cli.py speed auto (Options: auto, eco, 1, 2, 3, 4, 5)
  Set Airflow:          ./daikin_cli.py dir 3d     (Options: off, vertical, horizontal, 3d)
  Verified Shutdown:    ./daikin_cli.py force-off  (Retries until OFF)

get status: ./daikin_cli.py status

[DEVICE STATUS]
Power:    OFF
Mode:     Fan
Fan:      5 | Airflow: 3D
Inside:   22.0°C | Target: --°C
Outside:  24.0°C


