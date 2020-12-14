from common_files.common import *
from common_files.common_mcp23017 import *
from robot.api import logger
import logging
import smbus
import time

DELAY = 0.1  # 0.1 s delay
DELAY2 = 3  # 3 s delay
DELIMITER = 60

logging.basicConfig(level=logging.DEBUG)

class bcolors:
    GREEN = '\033[92m'
    BGREEN = '\033[1m' + '\033[92m'
    RED = '\033[91m'
    BRED = '\033[1m' + '\033[91m'
    YELLOW = '\033[93m'
    BYEL = '\033[1m' + '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class mcp23017:
	"""
	16-bit I/O Expander with I2C interface.
	"""

	_inst_counter = 0

	def __init__(self, addr=MCP23017_DEFAULT_ADDR):
		self.hardware_address = addr
		self.bus = smbus.SMBus(1)

		logger.info('MCP23017 configured hardware address: 0x{:02x}'.format(self.hardware_address))

		self.dispatcher = {I2C_IODIRA: self.set_bit_for_iodira, \
		                   I2C_IODIRB: self.set_bit_for_iodirb, \
		                   I2C_READ_PORT_A: self.read_port_A, \
		                   I2C_READ_PORT_B: self.read_port_B, \
		                   I2C_GPIOA: self.set_bit_for_gpioa, \
		                   I2C_GPIOB: self.set_bit_for_gpiob}

		self.port_A_dir_vector = 0xff  # direction is default set to input according to data sheet
		self.port_B_dir_vector = 0xff  # -"-
		self.port_A_pin_vector = 0x00
		self.port_B_pin_vector = 0x00

		mcp23017._inst_counter += 1
		self.id = mcp23017._inst_counter

	def configure(self, *params):
		#logger.info('MCP23017 Inst counter: {}'.format(self.id))
		rv = self.dispatcher[params[0]](params)
		return rv

	def set_bit_for_iodira(self, param):
		gpio_pin = param[1]
		mode = param[2]

		if mode == IN:
			self.port_A_dir_vector |= (1 << gpio_pin)
		elif mode == OUT:
			self.port_A_dir_vector &= ~(1 << gpio_pin)
		else:
			logger.warn('Invalid configuration of port A')

		logger.info('(i2c) Direction PortA - Pin: {}, mode: {}, Dir Vector: 0x{:02x}'.
		            format(gpio_pin, mcp23017_get_mode_name(mode), self.port_A_dir_vector))

		self.bus.write_byte_data(self.hardware_address, I2C_IODIRA, self.port_A_dir_vector)

	def set_bit_for_iodirb(self, param):
		gpio_pin = param[1]
		mode = param[2]

		if mode == IN:
			self.port_B_dir_vector |= (1 << gpio_pin)
		elif mode == OUT:
			self.port_B_dir_vector &= ~(1 << gpio_pin)
		else:
			logger.warn('Invalid configuration of port B')

		logger.info('(i2c) Direction PortB - Pin: {}, mode: {}, Dir Vector: 0x{:02x}'.
		            format(gpio_pin, mcp23017_get_mode_name(mode), self.port_B_dir_vector))

		self.bus.write_byte_data(self.hardware_address, I2C_IODIRB, self.port_B_dir_vector)

	def set_bit_for_gpioa(self, param):
		gpio_pin = param[1]
		level = param[2]

		if self.port_A_dir_vector & (1 << gpio_pin):
			logger.warn('(i2c) PortA, pin: {} is configured as input'.format(gpio_pin))
		else:
			if level == HIGH:
				self.port_A_pin_vector |= (1 << gpio_pin)
			elif level == LOW:
				self.port_A_pin_vector &= ~(1 << gpio_pin)
			else:
				logger.warn('(i2c) Invalid config, Use either LOW or HIGH for pin: {} at Port A'.
				            format(gpio_pin))

		logger.info('(i2c) Output PortA - Pin: {}, Level: {}, Pin Vector: 0x{:02x}'.
		            format(gpio_pin, level, self.port_A_pin_vector))

		self.bus.write_byte_data(self.hardware_address, I2C_GPIOA, self.port_A_pin_vector)

	def set_bit_for_gpiob(self, param):
		gpio_pin = param[1]
		level = param[2]

		if self.port_B_dir_vector & (1 << gpio_pin):
			logger.warn('(i2c) PortB, pin: {} is configured as input'.format(gpio_pin))
		else:
			if level == HIGH:
				self.port_B_pin_vector |= (1 << gpio_pin)
			elif level == LOW:
				self.port_B_pin_vector &= ~(1 << gpio_pin)
			else:
				logger.warn('(i2c) Invalid config, Use either LOW or HIGH for pin: {} at Port B'.
				            format(gpio_pin))

		logger.info('(i2c) Output PortB - Pin: {}, mode: {}, Pin Vector: 0x{:02x}'
		            .format(gpio_pin, level, self.port_B_pin_vector))

		self.bus.write_byte_data(self.hardware_address, I2C_GPIOB, self.port_B_pin_vector)

	def read_port_A(self, param):
		rv = self.bus.read_byte_data(self.hardware_address, I2C_GPIOA)
		logger.info('Read from MCP23017, port A - Reg: 0x{:02x}, Data: 0x{:02x}'.format(I2C_GPIOA, rv))

		return rv

	def read_port_B(self, param):
		rv = self.bus.read_byte_data(self.hardware_address, I2C_GPIOB)
		logger.info('Read from MCP23017, port B - Reg: 0x{:02x}, Data: 0x{:02x}'.format(I2C_GPIOB, rv))

		return rv

# --------------------------------------------------------------------------------
# Test purpose functions
# See document:
#    2/UMAN-610:00 00088,  Unicorn HW_SW structure and ...
#    CDIAG-200:01 00168, Schematics
#    MSPEC-610:00 00088, Raspberry Pi based produktion tester
#
#  Configuration of MCP23017 (U304) port A and B are done accordingly
#  to the current setup. See documentation above.
# --------------------------------------------------------------------------------
def config_port_A_addr_0(obj):
	obj.configure(I2C_IODIRA, I2C_GPA0, OUT)
	obj.configure(I2C_IODIRA, I2C_GPA1, OUT)
	obj.configure(I2C_IODIRA, I2C_GPA2, OUT)
	obj.configure(I2C_IODIRA, I2C_GPA3, OUT)
	obj.configure(I2C_IODIRA, I2C_GPA4, OUT)
	obj.configure(I2C_IODIRA, I2C_GPA5, OUT)
	obj.configure(I2C_IODIRA, I2C_GPA6, IN)
	obj.configure(I2C_IODIRA, I2C_GPA7, IN)

def config_port_B_addr_0(obj):
	obj.configure(I2C_IODIRB, I2C_GPB0, IN)
	obj.configure(I2C_IODIRB, I2C_GPB1, OUT)
	obj.configure(I2C_IODIRB, I2C_GPB2, OUT)
	obj.configure(I2C_IODIRB, I2C_GPB3, OUT)
	obj.configure(I2C_IODIRB, I2C_GPB4, OUT)
	obj.configure(I2C_IODIRB, I2C_GPB5, IN)
	obj.configure(I2C_IODIRB, I2C_GPB6, OUT)
	obj.configure(I2C_IODIRB, I2C_GPB7, OUT)

def turn_on_off_DC300V(obj):
	print(bcolors.BYEL+'Turn on DC300V'+bcolors.ENDC)
	obj.configure(I2C_GPIOA, I2C_GPA0, HIGH)
	time.sleep(DELAY2)
	print(bcolors.BYEL+'Turn off DC300V'+bcolors.ENDC)
	obj.configure(I2C_GPIOA, I2C_GPA0, LOW)

def turn_on_off_AC230V(obj):
	obj.configure(I2C_GPIOA, I2C_GPA1, HIGH)
	time.sleep(DELAY2)
	obj.configure(I2C_GPIOA, I2C_GPA1, LOW)

def turn_on_off_PE(obj):
	obj.configure(I2C_GPIOA, I2C_GPA2, HIGH)
	time.sleep(DELAY2)
	obj.configure(I2C_GPIOA, I2C_GPA2, LOW)

def turn_on_off_5Ve(obj):
	obj.configure(I2C_GPIOA, I2C_GPA3, HIGH)
	time.sleep(3)
	obj.configure(I2C_GPIOA, I2C_GPA3, LOW)

def turn_on_off_24V(obj):
	obj.configure(I2C_GPIOA, I2C_GPA4, HIGH)
	time.sleep(DELAY2)
	obj.configure(I2C_GPIOA, I2C_GPA4, LOW)

def turn_on_off_L1(obj):
	obj.configure(I2C_GPIOA, I2C_GPA5, HIGH)
	time.sleep(DELAY2)
	obj.configure(I2C_GPIOA, I2C_GPA5, LOW)

def turn_on_off_A0(obj):
	obj.configure(I2C_GPIOB, I2C_GPB1, HIGH)
	time.sleep(DELAY2)
	obj.configure(I2C_GPIOB, I2C_GPB1, LOW)

def turn_on_off_A1(obj):
	obj.configure(I2C_GPIOB, I2C_GPB2, HIGH)
	time.sleep(DELAY2)
	obj.configure(I2C_GPIOB, I2C_GPB2, LOW)

def turn_on_off_A2(obj):
	obj.configure(I2C_GPIOB, I2C_GPB3, HIGH)
	time.sleep(DELAY2)
	obj.configure(I2C_GPIOB, I2C_GPB3, LOW)

def turn_on_off_RESET(obj):
	obj.configure(I2C_GPIOB, I2C_GPB6, HIGH)
	time.sleep(DELAY2)
	obj.configure(I2C_GPIOB, I2C_GPB6, LOW)

def turn_on_off_SAFE(obj):
	obj.configure(I2C_GPIOB, I2C_GPB7, HIGH)
	time.sleep(DELAY2)
	obj.configure(I2C_GPIOB, I2C_GPB7, LOW)

def read_CLOSED(obj):
	rv = obj.read_port_A(I2C_GPIOA)
	print(rv)

def main():
	myMCP_0 = mcp23017(MCP23017_ADDR_0) # U304, see schematic, CDIAG-200:01 00168, PB2
	myMCP_1 = mcp23017(MCP23017_ADDR_1) # U303, see schematic

	# =========================================================
	# Below a number of test cases have been implemented.
	# To use them, comment/uncomment to select the test case
	# you want to run.
	# It's not always feasible to run all test cases at the 
	# same time. Just use one at a time.
	# =========================================================


	# ---------------------------------------------------------
	config_port_A_addr_0(myMCP_0)
	turn_on_off_DC300V(myMCP_0) # U304:21
	print(DELIMITER*'-')
	# ---------------------------------------------------------

	# ---------------------------------------------------------
	#config_port_A_addr_0(myMCP_0)
	#turn_on_off_AC230V(myMCP_0) # U304:22
	#print(DELIMITER*'-')
	# ---------------------------------------------------------

	# ---------------------------------------------------------
	#config_port_A_addr_0(myMCP_0)
	#turn_on_off_PE(myMCP_0) # U304:23
	#print(DELIMITER*'-')
	# ---------------------------------------------------------

	# ---------------------------------------------------------
	#config_port_A_addr_0(myMCP_0)
	#turn_on_off_5Ve(myMCP_0) # U304:24
	#print(DELIMITER*'-')
	# ---------------------------------------------------------

	# ---------------------------------------------------------
	#config_port_A_addr_0(myMCP_0)
	#turn_on_off_24V(myMCP_0) # U304:25
	#print(DELIMITER*'-')
	# ---------------------------------------------------------

	# ---------------------------------------------------------
	#config_port_A_addr_0(myMCP_0)
	#turn_on_off_L1(myMCP_0) # U304:26
	#print(DELIMITER*'-')
	# ---------------------------------------------------------

	# ---------------------------------------------------------
	#config_port_B_addr_0(myMCP_0)
	#turn_on_off_A0(myMCP_0) # U304:2
	#turn_on_off_A1(myMCP_0) # U304:3
	#turn_on_off_A2(myMCP_0) # U304:4
	#print(DELIMITER*'-')
	# ---------------------------------------------------------

	# ---------------------------------------------------------
	#config_port_B_addr_0(myMCP_0)
	#turn_on_off_RESET(myMCP_0) # U304:7
	#print(DELIMITER*'-')
	# ---------------------------------------------------------

	# ---------------------------------------------------------
	#config_port_B_addr_0(myMCP_0)
	#turn_on_off_SAFE(myMCP_0) # U304:8
	#print(DELIMITER*'-')
	# ---------------------------------------------------------

	# ---------------------------------------------------------
	#config_port_A_addr_0(myMCP_0)
	#read_CLOSED(myMCP_0) # U304:28
	#print(DELIMITER*'-')
	# ---------------------------------------------------------


if __name__ == '__main__':
	main()
