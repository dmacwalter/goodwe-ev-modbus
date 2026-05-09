DOMAIN = "goodwe_ev"

CONF_HOST = "host"
CONF_PORT = "port"
CONF_UNIT_ID = "unit_id"

DEFAULT_PORT = 502
DEFAULT_UNIT_ID = 247
SCAN_INTERVAL = 30  # seconds

# ── Register addresses ──────────────────────────────────────────────────────

REG_EMS_DISPATCH        = 10000  # RW  0=normal, 1=reduce to min power

REG_FAULT_01            = 10001  # RO  bitmask — AC faults
REG_FAULT_02            = 10002  # RO  bitmask — AC faults
REG_FAULT_03            = 10003  # RO  bitmask — AC faults
REG_FAULT_04            = 10004  # RO  reserved
REG_FAULT_05            = 10005  # RO  bitmask — AC alarms
REG_FAULT_06            = 10006  # RO  bitmask — AC alarms
REG_FAULT_07            = 10007  # RO  bitmask — HW faults
REG_FAULT_08            = 10008  # RO  reserved

REG_VOLT_A              = 10009  # RO  U16 ÷10 V
REG_VOLT_B              = 10010  # RO  U16 ÷10 V
REG_VOLT_C              = 10011  # RO  U16 ÷10 V
REG_CURR_A              = 10012  # RO  U16 ÷10 A
REG_CURR_B              = 10013  # RO  U16 ÷10 A
REG_CURR_C              = 10014  # RO  U16 ÷10 A
REG_POWER               = 10015  # RO  U16 ÷10 kW
REG_SESSION_ENERGY      = 10016  # RO  U16 ÷10 kWh
REG_STATUS              = 10017  # RO  enum (see CHARGER_STATUS)
REG_COMMS_STATUS        = 10018  # RO  bitmask

REG_PLUG_CHARGE         = 10019  # RW  0=off 1=on
REG_RESERVATION         = 10020  # RW  0=none 1=once 2=permanent

REG_SINGLE_3PH          = 10023  # RW  0=off 1=on
REG_MAINTAIN_MIN_PWR    = 10024  # RW  0=off 1=on
REG_DYN_LOAD_MGMT       = 10025  # RW  0=off 1=on

REG_MAX_CAPACITY        = 10027  # RW  U16 ÷10 kWh
REG_MIN_CAPACITY        = 10028  # RW  U16 ÷10 kWh
REG_MAX_POWER           = 10029  # RW  U16 ÷10 kW  [14,220]
REG_BATTERY_SOC         = 10030  # RW  U16 %  [0,100]
REG_CHARGING_MODE       = 10032  # RW  0=fast 1=PV 2=PV+bat
REG_GRID_LIMIT          = 10039  # RW  U16 ÷10 kW

REG_SN                  = 10040  # RO  STR 8 regs (16 bytes ASCII)
REG_SW_VERSION          = 10048  # RO  STR 2 regs
REG_SVN_VERSION         = 10050  # RO  U16
REG_HW_VERSION          = 10056  # RO  STR 2 regs
REG_POWER_SPEC          = 10058  # RO  0=7kW 1=11kW 2=22kW
REG_CHARGER_TYPE        = 10059  # RO  0=3-phase 1=single-phase

REG_CHARGE_CONTROL      = 10060  # RW  1=stop 2=start

REG_ACCUM_ENERGY        = 10065  # RO  U32 (2 regs) ÷10 kWh

REG_TIME_YM             = 10067  # RO  hi=year lo=month
REG_TIME_DH             = 10068  # RO  hi=day  lo=hour
REG_TIME_MS             = 10069  # RO  hi=min  lo=sec

REG_CAR_STATUS          = 10075  # RO  0=disconnected 1=half 2=connected
REG_START_MODE          = 10076  # RO  enum
REG_CHARGE_STRATEGY     = 10077  # RO  enum
REG_CP_STATE            = 10084  # RO  0-4 CP voltage level

REG_GREEN_ENERGY        = 10103  # RO  U32 (2 regs) ÷10 kWh
REG_GRID_ENERGY         = 10105  # RO  U32 (2 regs) ÷10 kWh
REG_POWER_SOURCE        = 10108  # RO  bitmask: bit0=grid bit1=PV bit2=bat

# ── Value maps ──────────────────────────────────────────────────────────────

CHARGER_STATUS = {
    0:  "idle_no_cable",
    1:  "idle_cable_connected",
    2:  "handshaking",
    3:  "charging",
    4:  "charge_complete",
    5:  "fault",
    6:  "scheduled",
    7:  "maintenance",
    8:  "start_failed",
    9:  "upgrading",
    10: "charging_interrupted",
}

CAR_STATUS = {
    0: "disconnected",
    1: "half_connected",
    2: "connected",
}

CP_STATE = {
    0: "no_voltage",
    1: "12v",
    2: "9v",
    3: "6v",
    4: "3v",
}

CHARGING_MODE = {
    0: "fast",
    1: "pv",
    2: "pv_battery",
}

POWER_SPEC = {0: "7kW", 1: "11kW", 2: "22kW"}
CHARGER_TYPE = {0: "three_phase", 1: "single_phase"}
