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
