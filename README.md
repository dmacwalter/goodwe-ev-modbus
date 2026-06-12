# GoodWe EV Charger — Home Assistant Integration

A local Modbus TCP integration for GoodWe AC EV chargers (HCA G2 series). No cloud, no app — direct communication over your local network.

## Requirements

- GoodWe AC EV charger reachable over Modbus TCP (default port 502)
- Charger firmware **V6 or newer** (reported by the charger as `6383`, i.e. V6.383) — energy consumption sensors do not work on earlier firmware
- Home Assistant 2024.1 or newer
- The charger's local IP address and Modbus Unit ID (default: **247**)

## Installation

### HACS (recommended)

1. Open HACS → Integrations → ⋮ menu → **Custom repositories**
2. Add `https://github.com/ondrej111/goodwe-ev-modbus` — category: **Integration**
3. Search for **GoodWe EV Charger** and install it
4. Restart Home Assistant

### Manual

Copy the `custom_components/goodwe_ev` folder into your HA `config/custom_components/` directory and restart.

## Configuration

Go to **Settings → Devices & Services → Add Integration** and search for **GoodWe EV Charger**.

| Field | Default | Description |
|---|---|---|
| IP Address | — | Local IP of the charger |
| Port | 502 | Modbus TCP port |
| Modbus Unit ID | 247 | Slave ID (check charger settings if unsure) |

## Entities

### Sensors (read-only)

| Entity | Unit | Description |
|---|---|---|
| Phase A/B/C Voltage | V | Per-phase AC voltage |
| Phase A/B/C Current | A | Per-phase charging current |
| Charging Power | kW | Total active charging power |
| Session Energy | kWh | Energy delivered in the current session |
| Total Energy | kWh | Cumulative energy delivered (all sessions) |
| Green Energy | kWh | Energy sourced from PV |
| Grid Energy | kWh | Energy sourced from the grid |
| Charger Status | — | idle, charging, fault, scheduled, … |
| Car Connection | — | disconnected / half connected / connected |
| CP State | — | Control pilot voltage level (A–E) |
| Charging Mode | — | Fast / PV only / PV + battery |
| Charger Type | — | Three-phase / Single-phase |
| Max Charging Power | kW | Currently configured power limit (readback) |
| Grid Power Limit | kW | Currently configured grid limit (readback) |

### Controls

| Entity | Type | Description |
|---|---|---|
| Charging | Switch | Start / stop a charging session |
| Plug & Charge | Switch | Enable automatic charging when cable is plugged in |
| EMS Dispatch (Reduce Power) | Switch | Reduce charger to minimum power on EMS command |
| Single/Three-Phase Switching | Switch | Toggle between single-phase and three-phase mode |
| Charging Mode | Select | Fast charging / PV only / PV + battery |
| Max Charging Power | Number | Set maximum charging power (1.4–22 kW) |
| Battery Discharge SOC Limit | Number | Minimum battery SOC before discharging to charger (0–100 %) |
| Grid Power Limit | Number | Maximum power draw from the grid (1.4–22 kW) |

## Notes

- Data is polled every **30 seconds** over Modbus TCP.
- The integration communicates **locally only** — no GoodWe cloud account needed.
- Energy consumption sensors (Total/Session/Green/Grid Energy) require charger firmware **V6 or newer**; the charger reports its firmware as `6383` (V6.383). On earlier firmware these sensors do not report.
- Total Energy resets to 0 if the charger's internal counter is cleared (e.g. factory reset).
- The Charging switch reads its state from Charger Status (status = charging), not from the command register, so it accurately reflects whether charging is actually in progress.

## Supported Models

Tested on the **GoodWe HCA G2** series (7 kW / 11 kW / 22 kW, single- and three-phase). Other GoodWe AC chargers using the same Modbus protocol may work but are untested.

## License

MIT
