#
# These are test cases used in mcp23s17.py, called from main().
# To run a test case comment/uncomment in mcp23s17.py the one
# you want to run.
#

from common_files.common import *
import time

class bcolors:
    GREEN = '\033[92m'
    BGRN = '\033[1m' + '\033[92m'
    RED = '\033[91m'
    BRED = '\033[1m' + '\033[91m'
    YELLOW = '\033[93m'
    BYEL = '\033[1m' + '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# ---------------------------------------------------------------------------
# U301
# The Uxyz:ab numbers are refering to the component number on the 
# Unicorn schematic, CDIAG-200:01 00168.

def inst_0_addr_0_port_A0_test(obj):
	"""
	Set Port A to output and set port 0 HIGH, wait 3 sec and set port LOW
	U301:21
	"""
	_MCP23S17_DEVICE_0 = '3'
	_MCP23S17_ADDR_0 = '0'
	_SPI_IOCON = '0x0a'
	_SPI_IODIRA = '0x00'
	_SPI_GPIOA = '0x12'
	_SPI_GPA0 = '0'
	_OUT = '0'
	_HI = '1'
	_LO = '0'

	print(bcolors.BYEL+'Set HAEN'+bcolors.ENDC)
	MCP_IOCON = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_IOCON}
	obj.configure(MCP_IOCON)

	print(bcolors.BYEL+'Configure Port A output'+bcolors.ENDC)
	MCP_PORT0 = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_IODIRA, 'Port':_SPI_GPA0, 'Mode':_OUT}
	obj.configure(MCP_PORT0)

	print(bcolors.BYEL+'*** Set Port A0 high, U301:21'+bcolors.ENDC)
	MCP_PORT0_HI = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_GPIOA, 'Port':_SPI_GPA0, 'Mode':_HI}
	obj.configure(MCP_PORT0_HI)
	time.sleep(DELAY_3s)

	print(bcolors.BYEL+'*** Set Port A0 low'+bcolors.ENDC)
	MCP_PORT0_LO = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_GPIOA, 'Port':_SPI_GPA0, 'Mode':_LO}
	obj.configure(MCP_PORT0_LO)

def inst_0_addr_0_port_A7_test(obj):
	"""
	Set Port A to output and set port 7 HIGH, wait 3 sec and set port LOW
	U301:28
	"""
	_MCP23S17_DEVICE_0 = '3'
	_MCP23S17_ADDR_0 = '0'
	_SPI_IOCON = '0x0a'
	_SPI_IODIRA = '0x00'
	_SPI_GPIOA = '0x12'
	_SPI_GPA7 = '7'
	_OUT = '0'
	_HI = '1'
	_LO = '0'

	print(bcolors.BYEL+'Set HAEN'+bcolors.ENDC)
	MCP_IOCON = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_IOCON}
	obj.configure(MCP_IOCON)

	print(bcolors.BYEL+'Configure Port A output'+bcolors.ENDC)
	MCP_PORT7 = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_IODIRA, 'Port':_SPI_GPA7, 'Mode':_OUT}
	obj.configure(MCP_PORT7)

	print(bcolors.BYEL+'*** Set Port A7 high, U301:28'+bcolors.ENDC)
	MCP_PORT7_HI = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_GPIOA, 'Port':_SPI_GPA7, 'Mode':_HI}
	obj.configure(MCP_PORT7_HI)
	time.sleep(DELAY_3s)

	print(bcolors.BYEL+'*** Set Port A7 low'+bcolors.ENDC)
	MCP_PORT7_LO = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_GPIOA, 'Port':_SPI_GPA7, 'Mode':_LO}
	obj.configure(MCP_PORT7_LO)

def inst_0_addr_0_port_B0_test(obj):
	"""
	Set DIO-8 to output. Set DIO-8 HIGH wait 3 sec and set DIO-8 LOW
	U301:1
	"""
	_MCP23S17_DEVICE_0 = '3'
	_MCP23S17_ADDR_0 = '0'
	_SPI_IOCON = '0x0a'
	_SPI_IODIRB = '0x01'
	_SPI_GPIOB = '0x13'
	_SPI_GPB0 = '0'
	_OUT = '0'
	_HI = '1'
	_LO = '0'

	print(bcolors.BYEL+'Set HAEN'+bcolors.ENDC)
	MCP_IOCON = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_IOCON}
	obj.configure(MCP_IOCON)

	print(bcolors.BYEL+'Configure Port B0 output, DIO-8'+bcolors.ENDC)
	MCP_PORT0 = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_IODIRB, 'Port':_SPI_GPB0, 'Mode':_OUT}
	obj.configure(MCP_PORT0)

	print(bcolors.BYEL+'*** Set Port B0 high, U301:1, DIO-8'+bcolors.ENDC)
	MCP_PORT0_HI = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_GPIOB, 'Port':_SPI_GPB0, 'Mode':_HI}
	obj.configure(MCP_PORT0_HI)
	time.sleep(DELAY_3s)

	print(bcolors.BYEL+'*** Set Port B0 low, DIO-8'+bcolors.ENDC)
	MCP_PORT0_LO = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_GPIOB, 'Port':_SPI_GPB0, 'Mode':_LO}
	obj.configure(MCP_PORT0_LO)

def inst_0_addr_0_port_B7_test(obj):
	"""
	Set Port B to output and set port 0 HIGH, wait 3 sec and set port LOW
	U301:8
	"""
	_MCP23S17_DEVICE_0 = '3'
	_MCP23S17_ADDR_0 = '0'
	_SPI_IOCON = '0x0a'
	_SPI_IODIRB = '0x01'
	_SPI_GPIOB = '0x13'
	_SPI_GPB7 = '7'
	_OUT = '0'
	_HI = '1'
	_LO = '0'

	print(bcolors.BYEL+'Set HAEN'+bcolors.ENDC)
	MCP_IOCON = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_IOCON}
	obj.configure(MCP_IOCON)

	print(bcolors.BYEL+'Configure Port B output'+bcolors.ENDC)
	MCP_PORT7 = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_IODIRB, 'Port':_SPI_GPB7, 'Mode':_OUT}
	obj.configure(MCP_PORT7)

	print(bcolors.BYEL+'*** Set Port B7 high, U301:8'+bcolors.ENDC)
	MCP_PORT7_HI = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_GPIOB, 'Port':_SPI_GPB7, 'Mode':_HI}
	obj.configure(MCP_PORT7_HI)
	time.sleep(DELAY_3s)

	print(bcolors.BYEL+'*** Set Port B7 low'+bcolors.ENDC)
	MCP_PORT7_LO = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_GPIOB, 'Port':_SPI_GPB7, 'Mode':_LO}
	obj.configure(MCP_PORT7_LO)

# ---------------------------------------------------------------------------
# U302
def inst_0_addr_1_port_A7_test(obj):
	"""
	Set Port A to output and set port 7 HIGH, wait 3 sec and set port LOW
	U302:28
	"""
	_MCP23S17_DEVICE_0 = '3'
	_MCP23S17_ADDR_1 = '1'
	_SPI_IOCON = '0x0a'
	_SPI_IODIRA = '0x00'
	_SPI_GPIOA = '0x12'
	_SPI_GPA7 = '7'
	_OUT = '0'
	_HI = '1'
	_LO = '0'

	print(bcolors.BYEL+'Set HAEN'+bcolors.ENDC)
	MCP_IOCON = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_IOCON}
	obj.configure(MCP_IOCON)

	MCP_PORT7 = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_IODIRA, 'Port':_SPI_GPA7, 'Mode':_OUT}
	obj.configure(MCP_PORT7)

	print(bcolors.BYEL+'*** Set Port A7 high, U302:28'+bcolors.ENDC)
	MCP_PORT7_HI = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_GPIOA, 'Port':_SPI_GPA7, 'Mode':_HI}
	obj.configure(MCP_PORT7_HI)

	time.sleep(DELAY_3s)

	print(bcolors.BYEL+'*** Set Port A low'+bcolors.ENDC)
	MCP_PORT7_LO = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_GPIOA, 'Port':_SPI_GPA7, 'Mode':_LO}
	obj.configure(MCP_PORT7_LO)

def inst_0_addr_1_port_A0_test(obj):
	"""
	Set Port A to output and set port 0 HIGH, wait 3 sec and set port LOW
	U302:21
	"""
	_MCP23S17_DEVICE_0 = '3'
	_MCP23S17_ADDR_1 = '1'
	_SPI_IOCON = '0x0a'
	_SPI_IODIRA = '0x00'
	_SPI_GPIOA = '0x12'
	_SPI_GPA0 = '0'
	_OUT = '0'
	_HI = '1'
	_LO = '0'

	print(bcolors.BYEL+'Set HAEN'+bcolors.ENDC)
	MCP_IOCON = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_IOCON}
	obj.configure(MCP_IOCON)

	MCP_PORT0 = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_IODIRA, 'Port':_SPI_GPA0, 'Mode':_OUT}
	obj.configure(MCP_PORT0)

	print(bcolors.BYEL+'*** Set Port A0 high, U302:21'+bcolors.ENDC)
	MCP_PORT0_HI = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_GPIOA, 'Port':_SPI_GPA0, 'Mode':_HI}
	obj.configure(MCP_PORT0_HI)

	time.sleep(DELAY_3s)

	print(bcolors.BYEL+'*** Set Port A0 low'+bcolors.ENDC)
	MCP_PORT0_LO = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_GPIOA, 'Port':_SPI_GPA0, 'Mode':_LO}
	obj.configure(MCP_PORT0_LO)

def inst_0_addr_1_port_B0_test(obj):
	"""
	Set Port B to output and set port 0 HIGH, wait 3 sec and set port LOW
	U302:1
	"""
	_MCP23S17_DEVICE_0 = '3'
	_MCP23S17_ADDR_1 = '1'
	_SPI_IOCON = '0x0a'
	_SPI_IODIRB = '0x01'
	_SPI_GPIOB = '0x13'
	_SPI_GPB0 = '0'
	_OUT = '0'
	_HI = '1'
	_LO = '0'

	print(bcolors.BYEL+'Set HAEN'+bcolors.ENDC)
	MCP_IOCON = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_IOCON}
	obj.configure(MCP_IOCON)

	MCP_PORT0 = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_IODIRB, 'Port':_SPI_GPB0, 'Mode':_OUT}
	obj.configure(MCP_PORT0)

	print(bcolors.BYEL+'*** Set Port B0 high, U302:28'+bcolors.ENDC)
	MCP_PORT0_HI = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_GPIOB, 'Port':_SPI_GPB0, 'Mode':_HI}
	obj.configure(MCP_PORT0_HI)

	time.sleep(DELAY_3s)

	print(bcolors.BYEL+'*** Set Port B0 low'+bcolors.ENDC)
	MCP_PORT0_LO = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_GPIOB, 'Port':_SPI_GPB0, 'Mode':_LO}
	obj.configure(MCP_PORT0_LO)

def inst_0_addr_1_port_B7_test(obj):
	"""
	Set Port B to output and set port 0 HIGH, wait 3 sec and set port LOW
	U302:8
	"""
	_MCP23S17_DEVICE_0 = '3'
	_MCP23S17_ADDR_1 = '1'
	_SPI_IOCON = '0x0a'
	_SPI_IODIRB = '0x01'
	_SPI_GPIOB = '0x13'
	_SPI_GPB7 = '7'
	_OUT = '0'
	_HI = '1'
	_LO = '0'

	print(bcolors.BYEL+'Set HAEN'+bcolors.ENDC)
	MCP_IOCON = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_IOCON}
	obj.configure(MCP_IOCON)

	MCP_PORT7 = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_IODIRB, 'Port':_SPI_GPB7, 'Mode':_OUT}
	obj.configure(MCP_PORT7)

	print(bcolors.BYEL+'*** Set Port B7 high, U302:28'+bcolors.ENDC)
	MCP_PORT7_HI = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_GPIOB, 'Port':_SPI_GPB7, 'Mode':_HI}
	obj.configure(MCP_PORT7_HI)

	time.sleep(DELAY_3s)

	print(bcolors.BYEL+'*** Set Port B7 low'+bcolors.ENDC)
	MCP_PORT7_LO = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_GPIOB, 'Port':_SPI_GPB7, 'Mode':_LO}
	obj.configure(MCP_PORT7_LO)


# ---------------------------------------------------------------------------
# U300
def inst_1_addr_0_port_A7_test(obj):
	"""
	Set Port A to output and set port 7 HIGH, wait 3 sec and set port LOW
	U300:28
	"""
	_MCP23S17_DEVICE_1 = '4'
	_MCP23S17_ADDR_0 = '0'
	_SPI_IOCON = '0x0a'
	_SPI_IODIRA = '0x00'
	_SPI_GPIOA = '0x12'
	_SPI_GPA7 = '7'
	_OUT = '0'
	_HI = '1'
	_LO = '0'

	print(bcolors.BYEL+'Set HAEN'+bcolors.ENDC)
	MCP_IOCON = {'Device':_MCP23S17_DEVICE_1, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_IOCON}
	obj.configure(MCP_IOCON)

	MCP_PORT7 = {'Device':_MCP23S17_DEVICE_1, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_IODIRA, 'Port':_SPI_GPA7, 'Mode':_OUT}
	obj.configure(MCP_PORT7)

	print(bcolors.BYEL+'*** Set Port A7 high, U300:28'+bcolors.ENDC)
	MCP_PORT7_HI = {'Device':_MCP23S17_DEVICE_1, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_GPIOA, 'Port':_SPI_GPA7, 'Mode':_HI}
	obj.configure(MCP_PORT7_HI)

	time.sleep(DELAY_3s)

	print(bcolors.BYEL+'*** Set Port A7 low'+bcolors.ENDC)
	MCP_PORT7_LO = {'Device':_MCP23S17_DEVICE_1, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_GPIOA, 'Port':_SPI_GPA7, 'Mode':_LO}
	obj.configure(MCP_PORT7_LO)

def inst_1_addr_0_port_A0_test(obj):
	"""
	Set Port A to output and set port 0 HIGH, wait 3 sec and set port LOW
	U300:21
	"""
	_MCP23S17_DEVICE_1 = '4'
	_MCP23S17_ADDR_0 = '0'
	_SPI_IOCON = '0x0a'
	_SPI_IODIRA = '0x00'
	_SPI_GPIOA = '0x12'
	_SPI_GPA0 = '0'
	_OUT = '0'
	_HI = '1'
	_LO = '0'

	print(bcolors.BYEL+'Set HAEN'+bcolors.ENDC)
	MCP_IOCON = {'Device':_MCP23S17_DEVICE_1, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_IOCON}
	obj.configure(MCP_IOCON)

	MCP_PORT0 = {'Device':_MCP23S17_DEVICE_1, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_IODIRA, 'Port':_SPI_GPA0, 'Mode':_OUT}
	obj.configure(MCP_PORT0)

	print(bcolors.BYEL+'*** Set Port A0 high, U300:28'+bcolors.ENDC)
	MCP_PORT0_HI = {'Device':_MCP23S17_DEVICE_1, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_GPIOA, 'Port':_SPI_GPA0, 'Mode':_HI}
	obj.configure(MCP_PORT0_HI)

	time.sleep(DELAY_3s)

	print(bcolors.BYEL+'*** Set Port A0 low'+bcolors.ENDC)
	MCP_PORT0_LO = {'Device':_MCP23S17_DEVICE_1, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_GPIOA, 'Port':_SPI_GPA0, 'Mode':_LO}
	obj.configure(MCP_PORT0_LO)

def inst_1_addr_0_port_B0_test(obj):
	"""
	Set Port B to output and set port 0 HIGH, wait 3 sec and set port LOW
	U300:1
	"""
	_MCP23S17_DEVICE_1 = '4'
	_MCP23S17_ADDR_0 = '0'
	_SPI_IOCON = '0x0a'
	_SPI_IODIRB = '0x01'
	_SPI_GPIOB = '0x13'
	_SPI_GPB0 = '0'
	_OUT = '0'
	_HI = '1'
	_LO = '0'

	print(bcolors.BYEL+'Set HAEN'+bcolors.ENDC)
	MCP_IOCON = {'Device':_MCP23S17_DEVICE_1, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_IOCON}
	obj.configure(MCP_IOCON)

	MCP_PORT0 = {'Device':_MCP23S17_DEVICE_1, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_IODIRB, 'Port':_SPI_GPB0, 'Mode':_OUT}
	obj.configure(MCP_PORT0)

	print(bcolors.BYEL+'*** Set Port B0 high, U300:1'+bcolors.ENDC)
	MCP_PORT0_HI = {'Device':_MCP23S17_DEVICE_1, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_GPIOB, 'Port':_SPI_GPB0, 'Mode':_HI}
	obj.configure(MCP_PORT0_HI)

	time.sleep(DELAY_3s)

	print(bcolors.BYEL+'*** Set Port B0 low'+bcolors.ENDC)
	MCP_PORT0_LO = {'Device':_MCP23S17_DEVICE_1, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_GPIOB, 'Port':_SPI_GPB0, 'Mode':_LO}
	obj.configure(MCP_PORT0_LO)

def inst_1_addr_0_port_B7_test(obj):
	"""
	Set Port B to output and set port 7 HIGH, wait 3 sec and set port LOW
	U300:8
	"""
	_MCP23S17_DEVICE_1 = '4'
	_MCP23S17_ADDR_0 = '0'
	_SPI_IOCON = '0x0a'
	_SPI_IODIRB = '0x01'
	_SPI_GPIOB = '0x13'
	_SPI_GPB7 = '7'
	_OUT = '0'
	_HI = '1'
	_LO = '0'

	print(bcolors.BYEL+'Set HAEN'+bcolors.ENDC)
	MCP_IOCON = {'Device':_MCP23S17_DEVICE_1, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_IOCON}
	obj.configure(MCP_IOCON)

	MCP_PORT7 = {'Device':_MCP23S17_DEVICE_1, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_IODIRB, 'Port':_SPI_GPB7, 'Mode':_OUT}
	obj.configure(MCP_PORT7)

	print(bcolors.BYEL+'*** Set Port B7 high, U300:8'+bcolors.ENDC)
	MCP_PORT7_HI = {'Device':_MCP23S17_DEVICE_1, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_GPIOB, 'Port':_SPI_GPB7, 'Mode':_HI}
	obj.configure(MCP_PORT7_HI)

	time.sleep(DELAY_3s)

	print(bcolors.BYEL+'*** Set Port B7 low'+bcolors.ENDC)
	MCP_PORT7_LO = {'Device':_MCP23S17_DEVICE_1, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_GPIOB, 'Port':_SPI_GPB7, 'Mode':_LO}
	obj.configure(MCP_PORT7_LO)

def inst_0_addr_1_mux_test(obj):
	"""
	Check MUX control on It's-It
	DIO_20 J5:14, DIO_21 J5:15, DIO_22:16, DIO_23:17
	Unicorn: GPA4-GP7 U302:25,26,27,28

	It's-It: V2_A0-V2_A3 U920:3,5,7,9
	                     U920:2,4,6,10
	"""
	_MCP23S17_DEVICE_0 = '3'
	_MCP23S17_ADDR_1 = '1'
	_IOCON_HAEN = '0x0a'
	_SPI_IODIRA = '0x00'
	_SPI_GPIOA = '0x12'
	_SPI_GPA = '7'      # Change port number to 4,5,6,7
	_OUT = '0'
	_HI = '1'
	_LO = '0'

	print(bcolors.BYEL+'Set HAEN'+bcolors.ENDC)
	IOCON_HAEN = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_IOCON_HAEN}
	obj.configure(IOCON_HAEN)

	PORT_OUT = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_IODIRA, 'Port':_SPI_GPA, 'Mode':_OUT}
	obj.configure(PORT_OUT)

	print(bcolors.BYEL+'*** Set Port A4 high, U302:25'+bcolors.ENDC)
	MCP_PORT_HI = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_GPIOA, 'Port':_SPI_GPA, 'Mode':_HI}
	obj.configure(MCP_PORT_HI)

	time.sleep(DELAY_3s)

	print(bcolors.BYEL+'*** Set Port A low'+bcolors.ENDC)
	MCP_PORT_LO = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_GPIOA, 'Port':_SPI_GPA, 'Mode':_LO}
	obj.configure(MCP_PORT_LO)

def inst_1_addr_0_port_B_read(obj):
	"""
	Set Port B to input
	U300
	"""
	_MCP23S17_DEVICE_1 = '4'
	_MCP23S17_ADDR_0 = '0'
	_SPI_IOCON = '0x0a'
	_SPI_IODIRB = '0x01'
	_SPI_GPIOB = '0x13'
	_IN = '0'

	print(bcolors.BYEL+'Set HAEN'+bcolors.ENDC)
	MCP_IOCON = {'Device':_MCP23S17_DEVICE_1, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_IOCON}
	obj.configure(MCP_IOCON)

	MCP_PORT_B = {'Device':_MCP23S17_DEVICE_1, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_IODIRB, 'Port': 0, 'Mode':_IN}
	obj.configure(MCP_PORT_B)

	item = {'Device':_MCP23S17_DEVICE_1, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':'0x99'}
	obj.configure(item)

	time.sleep(DELAY_3s)
