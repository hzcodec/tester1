# pylint: disable= no-else-return

from common_files.common_mcp23017 import *
from common_files.common_mcp23s17 import *
from common_files.common_ad4112 import *
from common_files.common_dac61408 import *

DELAY_01s = 0.1
DELAY_02s = 0.2
DELAY_05s = 0.5
DELAY_1s = 1
DELAY_2s = 2
DELAY_3s = 3

# Misc defines
MCP23017_DEFAULT_ADDR = 0x20
MCP23017_ADDR_0 = 0x20
MCP23017_ADDR_1 = 0x21

# SPI defines
SPI_MCP23S17_DEVICE = 2 # SPI1_CE2
SPI_MCP23S17_PORT = 1
SPI_LOW_SPEED = 40000  # lowered the speed for test purpose
SPI_HIGH_SPEED = 1000000

SPI_MODE_0 = 0b00
SPI_MODE_1 = 0b01
SPI_MODE_2 = 0b10
SPI_MODE_3 = 0b11

DUMMY_BYTE = 0x00
PADDING_BYTE = 0x00

PULLUP = 1 # Pullup enable. N.B! It's not possible to enable individual ports
NONE = 0

# in/out mode
IN = 1
OUT = 0


# on/off mode
OFF = 0
ON = 1

# PLC Digital output references
DO1 = 1
DO2 = 2
DO3 = 3
DO4 = 4
DO5 = 5
DO6 = 6
DO_PORTS = [DO1, DO2, DO3, DO4, DO5, DO6]

DOC1 = 1
DOC2 = 2
DOC3 = 3
DOC4 = 4
DOC5 = 5
DOC6 = 6
DOC7 = 7
DOC_PORTS = [DOC1, DOC2, DOC3, DOC4, DOC5, DOC6, DOC7]


# level
HIGH = 1
LOW = 0

ERROR_MSG = 'Err: Invalid input'
MEAS_CURR = 0
MEAS_VOLT = 1
MEAS_DIFF = 2

# Relay index controlled by MCP23017 (addr=0)
DC_300V = 0
AC_230V = 1
PROTECTED_EARTH = 2
p_24V = 3
p_5Ve = 4
L1 = 5

# port B
S1 = 0
S2 = 1
READY = 2
SAFE =  3
RESET = 4


# Relay names controlled by MCP23017 (addr=1)
RELAY1 = 0
RELAY2 = 1
RELAY3 = 2
RELAY4 = 3
RELAY5 = 4
RELAY6 = 5
RELAY7 = 6
RELAY8 = 7
RELAY9 = 8
RELAY10 =9
RELAY11 = 10
RELAY12 = 11
RELAY13 = 12
RELAY14 = 13
RELAY15 = 14
RELAY16 = 15


# -------------------------------------------------------------
# Device parameters
# -------------------------------------------------------------
DAC61408_DEVICE = 0
AD4112_DEVICE_0 = 1
AD4112_DEVICE_1 = 2
MCP23S17_DEVICE_0 = 3
MCP23S17_DEVICE_1 = 4

MCP23S17_ADDR_0 = 0
MCP23S17_ADDR_1 = 1

SPI_ADDRESS_0 = 0
SPI_ADDRESS_1 = 1


# ------------------------------------------------------------------
# help functions
# ------------------------------------------------------------------
def mcp23017_get_mode_name(inp):
	if inp == OUT:
		return 'OUT'
	else:
		return 'IN'

def mcp23017_get_level_name(inp):
	if inp == ON:
		return 'ON'
	else:
		return 'OFF'

def mcp23017_get_power_name(inp):
	if inp == DC_300V:
		return 'DC_300V'
	elif inp == AC_230V:
		return 'AC_230V'
	elif inp == PROTECTED_EARTH:
		return 'PROTECTED_EARTH'
	elif inp == p_24V:
		return 'p_24V'
	elif inp == p_5Ve:
		return 'p_5Ve'
	elif inp == L1:
		return 'L1'
	else:
		return 'OFF'

def mcp23017_get_device_name(inp):
	if inp == 0:
		return 'DAC61408 device'
	elif inp == 1:
		return 'AD4112 device 0'
	elif inp == 2:
		return 'AD4112 device 1'
	elif inp == 3:
		return 'MCP23S17 device 0'
	elif inp == 4:
		return 'MCP23S17 device 1'
	else:
		return ERROR_MSG

def mcp23s17_get_device_name(inp):
	if inp == 3:
		return 'MCP23S17_DEVICE_0'
	elif inp == 4:
		return 'MCP23S17_DEVICE_1'
	else:
		return ERROR_MSG

def mcp23017_get_pullup_mode(inp):
	if inp == PULLUP:
		return 'PULLUP ENABLED'
	else:
		return ERROR_MSG

