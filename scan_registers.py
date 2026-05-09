#!/usr/bin/env python3
"""Scan Modbus registers on a Goodwe EV charger — discovers unit ID and live registers."""

import argparse
import logging
import sys
import time
from pymodbus.client import ModbusTcpClient, ModbusUdpClient

# Suppress pymodbus noise
logging.getLogger("pymodbus").setLevel(logging.CRITICAL)

HOST = "192.168.33.26"
PORT = 502
CHUNK = 10
DELAY = 0.2  # seconds between requests


def try_read(client, func, address, count, unit, delay=DELAY):
    time.sleep(delay)
    try:
        if func == "holding":
            r = client.read_holding_registers(address, count=count, device_id=unit)
        else:
            r = client.read_input_registers(address, count=count, device_id=unit)
        if r.isError():
            return None
        return r.registers
    except Exception:
        return None


def probe_unit_id(client, delay):
    """Try common unit IDs with single-register reads; return the first one that answers."""
    for uid in [1, 0, 2, 247, 255]:
        print(f"  Trying unit ID {uid} ...", end=" ", flush=True)
        for start in [0, 40000, 1000, 100, 45000]:
            regs = try_read(client, "holding", start, 1, uid, delay)
            if regs is not None:
                print(f"responded at holding register {start}")
                return uid, start
        print("no response")
    return None, None


def scan(client, func, start, end, unit, chunk, delay):
    """Scan [start, end) in chunks; return dict of address->value for non-error registers."""
    results = {}
    pos = start
    consecutive_empty = 0
    while pos < end:
        length = min(chunk, end - pos)
        regs = try_read(client, func, pos, length, unit, delay)
        if regs is None:
            consecutive_empty += 1
            if consecutive_empty >= 8:
                pos += chunk * 4  # skip ahead over large dead zone
                consecutive_empty = 0
                continue
        else:
            consecutive_empty = 0
            for i, v in enumerate(regs):
                results[pos + i] = v
        pos += length
    return results


def print_table(title, data):
    if not data:
        print(f"\n  {title}: no registers responded")
        return
    print(f"\n{'='*64}")
    print(f"  {title}")
    print(f"{'='*64}")
    print(f"{'Reg':>6}  {'Dec':>6}  {'Hex':>6}  {'Binary':>16}  Signed")
    print(f"{'-'*6}  {'-'*6}  {'-'*6}  {'-'*16}  {'-'*6}")
    for reg, val in sorted(data.items()):
        signed = val if val < 0x8000 else val - 0x10000
        print(f"{reg:>6}  {val:>6}  {val:#06x}  {val:016b}  {signed:>6}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=HOST)
    parser.add_argument("--port", type=int, default=PORT)
    parser.add_argument("--unit",  type=int,   default=None, help="Force unit ID (skip probe)")
    parser.add_argument("--start", type=int,   default=0)
    parser.add_argument("--end",   type=int,   default=2000)
    parser.add_argument("--delay", type=float, default=DELAY,
                        help="Seconds between requests (default 0.2)")
    parser.add_argument("--chunk", type=int,   default=CHUNK,
                        help="Registers per request (default 10)")
    parser.add_argument("--timeout", type=float, default=5.0,
                        help="Socket timeout in seconds (default 5)")
    parser.add_argument("--udp", action="store_true",
                        help="Use UDP instead of TCP")
    args = parser.parse_args()

    proto = "UDP" if args.udp else "TCP"
    print(f"Connecting via Modbus {proto} to {args.host}:{args.port}  timeout={args.timeout}s  delay={args.delay}s ...")
    if args.udp:
        client = ModbusUdpClient(args.host, port=args.port, timeout=args.timeout)
    else:
        client = ModbusTcpClient(args.host, port=args.port, timeout=args.timeout)
    if not client.connect():
        print("ERROR: connection failed.", file=sys.stderr)
        sys.exit(1)
    print("Connected.\n")

    if args.unit is not None:
        unit = args.unit
        print(f"Using forced unit ID {unit}")
    else:
        print("Probing unit IDs (trying 1, 0, 2, 247, 255) ...")
        unit, _ = probe_unit_id(client, args.delay)
        if unit is None:
            print("\nNo unit responded. Suggestions:")
            print("  python3 scan_registers.py --unit 1 --delay 0.5")
            print("  python3 scan_registers.py --unit 0 --delay 0.5")
            client.close()
            sys.exit(1)
        print(f"Using unit ID: {unit}\n")

    print(f"Scanning holding registers {args.start}–{args.end} (chunk={args.chunk}) ...")
    holding = scan(client, "holding", args.start, args.end, unit, args.chunk, args.delay)
    print(f"  Found {len(holding)} holding registers with values")

    print(f"Scanning input registers {args.start}–{args.end} (chunk={args.chunk}) ...")
    inp = scan(client, "input", args.start, args.end, unit, args.chunk, args.delay)
    print(f"  Found {len(inp)} input registers with values")

    client.close()

    print_table(f"Holding Registers FC3  [{args.start}–{args.end}]  unit={unit}  {proto}", holding)
    print_table(f"Input Registers   FC4  [{args.start}–{args.end}]  unit={unit}  {proto}", inp)

    print("\nDone.")


if __name__ == "__main__":
    main()
