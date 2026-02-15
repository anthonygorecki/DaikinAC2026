#!/usr/bin/env python3
import asyncio
import os
import sys
import argparse
from daikin_legacy import DaikinLegacy

def load_config():
    conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "daikin.conf")
    config = {}
    if not os.path.exists(conf_path):
        print(f"ERROR: Configuration file not found at {conf_path}")
        print("Setup REQUIRED: Please create 'daikin.conf' with IP_ADDRESS and MY_UUID.")
        sys.exit(1)
    
    with open(conf_path, "r") as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                key, val = line.strip().split("=", 1)
                config[key] = val
    
    if "IP_ADDRESS" not in config or "MY_UUID" not in config:
        print("ERROR: daikin.conf is missing IP_ADDRESS or MY_UUID.")
        sys.exit(1)
    return config

async def display_status(hc):
    res = await hc.get_status()
    print(f"\n[DEVICE STATUS]")
    print(f"Power:    {res.get('pow', '??')}")
    print(f"Mode:     {res.get('mode', '??')}")
    print(f"Fan:      {res.get('f_rate', '??')} | Airflow: {res.get('f_dir', '??')}")
    print(f"Inside:   {res.get('htemp', '--')}°C | Target: {res.get('stemp', '--')}°C")
    print(f"Outside:  {res.get('otemp', '--')}°C\n")

async def main():
    conf = load_config()
    usage_examples = """
EXAMPLES:
  Set Fan Speed:        ./daikin_cli.py speed auto (Options: auto, eco, 1, 2, 3, 4, 5)
  Set Airflow:          ./daikin_cli.py dir 3d     (Options: off, vertical, horizontal, 3d)
  Verified Shutdown:    ./daikin_cli.py force-off  (Retries until OFF)
    """

    parser = argparse.ArgumentParser(
        prog="daikin_cli",
        description="CLI for Daikin BRP069B41 matching official app terminology.",
        epilog=usage_examples,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", help="Available Commands")
    subparsers.add_parser("status", help="Show all current settings")
    subparsers.add_parser("on", help="Power ON")
    subparsers.add_parser("off", help="Power OFF (Standard)")
    subparsers.add_parser("force-off", help="Attempt shutdown with verification and retries")

    speed_map = {"auto": "A", "eco": "B", "1": "3", "2": "4", "3": "5", "4": "6", "5": "7"}
    speed_parser = subparsers.add_parser("speed", help="Set Fan Speed")
    speed_parser.add_argument("val", choices=speed_map.keys())

    dir_map = {"off": "0", "vertical": "1", "horizontal": "2", "3d": "3"}
    dir_parser = subparsers.add_parser("dir", help="Set Airflow Swing")
    dir_parser.add_argument("val", choices=dir_map.keys())

    modes = {"cool": "3", "heat": "4", "dry": "2", "fan": "6"}
    for mode in modes:
        p = subparsers.add_parser(mode, help=f"Set to {mode.upper()} mode")
        p.add_argument("temp", type=str, nargs="?", default=None, help="Target Temperature")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    hc = DaikinLegacy(conf["IP_ADDRESS"], conf["MY_UUID"])

    try:
        if args.command == "status":
            await display_status(hc)
        elif args.command == "on":
            await hc.set_state(pow="1")
            await display_status(hc)
        elif args.command == "off":
            await hc.set_state(pow="0")
            await display_status(hc)
        elif args.command == "force-off":
            for attempt in range(1, 6):
                print(f"Shutdown Attempt {attempt}...")
                await hc.set_state(pow="0")
                await asyncio.sleep(5)
                res = await hc.get_status()
                if res.get('pow') == 'OFF':
                    print("--- [SUCCESS] Shutdown Verified ---")
                    return
                print("--- [RETRYING] Unit still reports ON ---")
            print("--- [FAILURE] Could not verify shutdown ---")
            sys.exit(1)
        elif args.command == "speed":
            await hc.set_state(f_rate=speed_map[args.val])
            await display_status(hc)
        elif args.command == "dir":
            await hc.set_state(f_dir=dir_map[args.val])
            await display_status(hc)
        elif args.command in modes:
            await hc.set_state(mode=modes[args.command], stemp=args.temp)
            await display_status(hc)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
