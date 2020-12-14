# pylint: disable= line-too-long
# pylint: disable= unused-variable
# pylint: disable= wrong-import-order
from common_files.common import *
from common_files.common_mcp23s17 import *
from robot.api import logger
import logging
import os
import spidev
import time
import mcp23s17_test as mcpt  # test functions for MCP23S17 used by main

logging.basicConfig(level=logging.DEBUG)

SPI_PORT = 0
SPI_DEVICE = 0 # SPI0_CE0

READ_OP_CODE = 0x41
WRITE_OP_CODE = 0x40
WRITE_OP_CODE_ADDR_1 = 0x42
SHIFT_CTRL_BIT = 1
DUMMY = 0  # just to fit the parameters at function call
SECOND_BYTE = 2  # valid byte in list at read operation
ALL_PORTS_INPUTS = 0xff
ALL_PORTS_OUTPUTS = 0x00


class bcolors:
    GREEN = '\033[92m'
    BGRN = '\033[1m' + '\033[92m'
    RED = '\033[91m'
    BRED = '\033[1m' + '\033[91m'
    YELLOW = '\033[93m'
    BYEL = '\033[1m' + '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class mcp23s17():
	def __init__(self):
		"""
		create four instances since there are two sets of devices.
		Each set contains two devices of MCP23S17 with its corresponding address,
		ADDR=0 and ADDR=1.
		"""
		self.mcp_inst_0_addr_0 = mcp23s17_internal()
		self.mcp_inst_0_addr_1 = mcp23s17_internal()
		self.mcp_inst_1_addr_0 = mcp23s17_internal()

		# Only used if an instance of the chip is mounted. See also comment below.
		#self.mcp_inst_1_addr_1 = mcp23s17_internal('Inst1, Addr 1', 1)

	def configure(self, *params):

		#logger.info('Select MCP23S17 to configure: {}'.format(params))
		device = int(params[0]['Device'])
		addr = int(params[0]['SPI-addr'])

		if device == MCP23S17_DEVICE_0:
			if addr == MCP23S17_ADDR_0:
				logger.info('Configure MCP23S17_DEVICE_0, ADDR0')
				rv = self.mcp_inst_0_addr_0.configure_mcp(params)
				return rv
			else:
				logger.info('Configure MCP23S17_DEVICE_0, ADDR1')
				rv = self.mcp_inst_0_addr_1.configure_mcp(params)
				return rv

		elif device == MCP23S17_DEVICE_1:
			if addr == MCP23S17_ADDR_0:
				logger.info('Configure MCP23S17_DEVICE_1, ADDR0')
				rv = self.mcp_inst_1_addr_0.configure_mcp(params)
				return rv
			else:
				# Only used if an instance of the chip is mounted
				#self.mcp_inst_1_addr_1.configure_mcp(params)
				logger.warn('Chip does not exists!')
		else:
			logger.warn('Nothing is selected')

	def get_vector(self):
		"""
		Used for test purpose. To get track of internal vectors.
		"""
		rv1, rv2 = self.mcp_inst_0_addr_0.get_dir_vectors()
		rv3, rv4 = self.mcp_inst_0_addr_0.get_pin_vectors()
		print('MCP0, Addr 0, Direction vector A: 0x{:02x}'.format(rv1))
		print('MCP0, Addr 0, Pin vector A: 0x{:02x}'.format(rv3))
		print('MCP0, Addr 0, Direction vector B: 0x{:02x}'.format(rv2))
		print('MCP0, Addr 0, Pin vector B: 0x{:02x}'.format(rv4))


		rv1, rv2 = self.mcp_inst_0_addr_1.get_dir_vectors()
		rv3, rv4 = self.mcp_inst_0_addr_1.get_pin_vectors()
		print('MCP0, Addr 1, Direction vector A: 0x{:02x}'.format(rv1))
		print('MCP0, Addr 1, Pin vector A: 0x{:02x}'.format(rv3))
		print('MCP0, Addr 1, Direction vector B: 0x{:02x}'.format(rv2))
		print('MCP0, Addr 1, Pin vector B: 0x{:02x}'.format(rv4))

		print('----------------')
		rv1, rv2 = self.mcp_inst_1_addr_0.get_dir_vectors()
		rv3, rv4 = self.mcp_inst_1_addr_0.get_pin_vectors()
		print('MCP1, Addr 0, Direction vector A: 0x{:02x}'.format(rv1))
		print('MCP1, Addr 0, Pin vector A: 0x{:02x}'.format(rv3))
		print('MCP1, Addr 0, Direction vector B: 0x{:02x}'.format(rv2))
		print('MCP1, Addr 0, Pin vector B: 0x{:02x}'.format(rv4))


class mcp23s17_internal:
	def __init__(self):
		self.spi = spidev.SpiDev()
		self.spi.open(SPI_PORT, SPI_DEVICE)
		self.spi.max_speed_hz = SPI_HIGH_SPEED
		self.spi.mode = SPI_MODE_0

		self.dispatcher = {SPI_IODIRA: self._set_bit_for_iodira,
		                   SPI_IODIRB: self._set_bit_for_iodirb,
		                   SPI_GPIOA: self._set_bit_for_gpioa,
		                   SPI_GPIOB: self._set_bit_for_gpiob,
		                   SPI_IOCON: self._set_haen,
		                   SPI_GPPUA: self._set_pullup_for_gpioa,
		                   SPI_GPPUB: self._set_pullup_for_gpiob,
		                   SPI_READ_A: self._read_gpioa,
		                   SPI_READ_B: self._read_gpiob,
		                   SPI_OPTO_A_IN: self._config_opto_a_in,
		                   SPI_OPTO_B_IN: self._config_opto_b_in,
		                   SPI_OPTO_B_OUT: self._config_opto_b_out,
		                   SPI_GPB_C: self._set_gpb_port_c}

		self.port_A_dir_vector = 0xff  # direction is default set to input according to data sheet (1 = IN, 0 = OUT)
		self.port_B_dir_vector = 0xff  # -"-
		self.port_A_pin_vector = 0x00
		self.port_B_pin_vector = 0x00

	def configure_mcp(self, params):
		reg = int(params[0]['Reg'], 16)
		#logger.info('Reg in config_mcp: {}'.format(hex(reg)))

		rv = self.dispatcher[reg](params)
		return rv

	def _config_opto_a_in(self, param):
		logger.info('config_opto A in, param:{}, Command: [0x{:02x} 0x{:02x} 0x{:02x}]'.format(param, WRITE_OP_CODE, SPI_IODIRA, ALL_PORTS_INPUTS))
		self.spi.xfer2([WRITE_OP_CODE, SPI_IODIRA, ALL_PORTS_INPUTS])

	def _config_opto_b_in(self, param):
		logger.info('config_opto B in, param:{}, Command: [0x{:02x} 0x{:02x} 0x{:02x}]'.format(param, WRITE_OP_CODE, SPI_IODIRB, ALL_PORTS_INPUTS))
		self.spi.xfer2([WRITE_OP_CODE, SPI_IODIRB, ALL_PORTS_INPUTS])

	def _config_opto_b_out(self, param):
		logger.info('config_opto B out, param:{}, Command: [0x{:02x} 0x{:02x} 0x{:02x}]'.format(param, WRITE_OP_CODE, SPI_IODIRB, 0x00))
		self.spi.xfer2([WRITE_OP_CODE, SPI_IODIRB, ALL_PORTS_OUTPUTS])

	def _set_gpb_port_c(self, param):
		data = int(param[0]['Data'])
		logger.info('param for port C: 0x{:02x}'.format(data))

		logger.info('config_opto B out, param:{}, Command: [0x{:02x} 0x{:02x} 0x{:02x}]'.format(param, WRITE_OP_CODE_ADDR_1, SPI_IODIRB, data))
		self.spi.xfer2([WRITE_OP_CODE_ADDR_1, SPI_GPIOB, ALL_PORTS_OUTPUTS])

	def _set_bit_for_iodira(self, param):
		logger.info('Set bit for IODIRA: {}'.format(param))
		device = int(param[0]['Device'])
		addr = int(param[0]['SPI-addr'])
		gpio_pin = int(param[0]['Port'])
		mode = int(param[0]['Mode'])

		# SPI control byte format
		# bit no:  | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
		# value:   | 0 | 1 | 0 | 0 | a | b | c | 0 |
		#                          |<--------->|
		#                              addr
		#                                        WR

		# Device is either 0x011 or 0x100. so bit 2 is used to set up the slave addres
		control_byte = WRITE_OP_CODE | (addr << SHIFT_CTRL_BIT)
		logger.info('control_byte for IODIRA: 0x{:02x}'.format(control_byte))

		if mode == IN:
			self.port_A_dir_vector |= (1 << gpio_pin)
		elif mode == OUT:
			self.port_A_dir_vector &= ~(1 << gpio_pin)
		else:
			logger.warn('Invalid config of IODIRA')

		logger.info('(spi) Device: {},  Addr {} - Pin: {}, mode: {}, Dir Vector A: 0x{:02x}'
		            .format(device, addr, gpio_pin, mode, self.port_A_dir_vector))

		self.spi.mode = SPI_MODE_0
		self.spi.writebytes([control_byte, SPI_IODIRA, self.port_A_dir_vector])

	def _set_bit_for_iodirb(self, param):
		logger.info('Set bit for IODIRB: {}'.format(param))
		device = int(param[0]['Device'])
		addr = int(param[0]['SPI-addr'])
		gpio_pin = int(param[0]['Port'])
		mode = int(param[0]['Mode'])

		# SPI control byte format
		# bit no:  | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
		# value:   | 0 | 1 | 0 | 0 | a | b | c | 0 |
		#                          |<--------->|
		#                              addr
		#                                        WR

		# Device is either 0x011 or 0x100. so bit 2 is used to set up the slave addres
		control_byte = WRITE_OP_CODE | (addr << SHIFT_CTRL_BIT)
		#print('control_byte for IODIRB: 0x{:02x}'.format(control_byte))

		if mode == IN:
			self.port_B_dir_vector |= (1 << gpio_pin)
		elif mode == OUT:
			self.port_B_dir_vector &= ~(1 << gpio_pin)
		else:
			logger.warn('Invalid config of IODIRB')

		logger.info('(spi) Device: {},  Addr {} - Pin: {}, mode: {}, Dir Vector B: 0x{:02x}'
		            .format(device, addr, gpio_pin, mode, self.port_B_dir_vector))

		self.spi.mode = SPI_MODE_0
		self.spi.writebytes([control_byte, SPI_IODIRB, self.port_B_dir_vector])

	def _set_bit_for_gpioa(self, param):
		logger.info('Set bit for GPIOA: {}'.format(param))
		device = int(param[0]['Device'])
		addr = int(param[0]['SPI-addr'])
		gpio_pin = int(param[0]['Port'])
		level = int(param[0]['Mode'])

		control_byte = WRITE_OP_CODE | (addr << SHIFT_CTRL_BIT)
		logger.info('control_byte for GPIOA: 0x{:02x}'.format(control_byte))

		if self.port_A_dir_vector & (1 << gpio_pin):
			logger.warn('PortA {} is configured as input'.format(gpio_pin))
		else:
			if level == HIGH:
				self.port_A_pin_vector |= (1 << gpio_pin)
			elif level == LOW:
				self.port_A_pin_vector &= ~(1 << gpio_pin)
			else:
				logger.warn('(spi) Invalid config, Use either LOW or HIGH for pin: {} at Port A'.format(gpio_pin))

		logger.info('(spi) Device: {},  Addr {} - Pin: {}, Level: {}, Pin Vector A: 0x{:02x}'
		            .format(device, addr, gpio_pin, level, self.port_A_pin_vector))

		self.spi.mode = SPI_MODE_0
		self.spi.writebytes([control_byte, SPI_GPIOA, self.port_A_pin_vector])

	def _set_bit_for_gpiob(self, param):
		logger.info('Set bit for GPIOB: {}'.format(param))
		device = int(param[0]['Device'])
		addr = int(param[0]['SPI-addr'])
		gpio_pin = int(param[0]['Port'])
		level = int(param[0]['Mode'])

		control_byte = WRITE_OP_CODE | (addr << SHIFT_CTRL_BIT)
		logger.info('control_byte for GPIOB: 0x{:02x}'.format(control_byte))

		if self.port_B_dir_vector & (1 << gpio_pin):
			logger.warn('(spi) PortB {} is configured as input'.format(gpio_pin))
		else:
			if level == HIGH:
				self.port_B_pin_vector |= (1 << gpio_pin)
			elif level == LOW:
				self.port_B_pin_vector &= ~(1 << gpio_pin)
			else:
				print('(spi) Invalid config, Use either LOW or HIGH for pin: {} at Port B'.format(gpio_pin))

		logger.info('(spi) Device: {},  Addr {} - Pin: {}, Level: {}, Pin Vector B: 0x{:02x}'
		            .format(device, addr, gpio_pin, level, self.port_B_pin_vector))

		self.spi.mode = SPI_MODE_0
		self.spi.writebytes([control_byte, SPI_GPIOB, self.port_B_pin_vector])

	def _set_haen(self, param):
		addr = int(param[0]['SPI-addr'])
		control_byte = WRITE_OP_CODE | (addr << SHIFT_CTRL_BIT)
		logger.info('Enable HAEN for addr: {}, control_byte: 0x{:01x}'.format(addr, control_byte))

		self.spi.writebytes([control_byte, SPI_IOCON, 0x08])
		time.sleep(0.1)

		# ---------------------------------------------------------------------
		# This is just a check of IOCON register for debugging purpose
		#
		control_byte = READ_OP_CODE | (addr << SHIFT_CTRL_BIT)

		self.spi.mode = SPI_MODE_0
		rv = self.spi.xfer2([control_byte, SPI_IOCON, 0x00])
		logger.info('Read SPI reg IOCON: 0x{:02x}, control_byte: 0x{:01x}'.format(rv[SECOND_BYTE], control_byte))

		if rv[SECOND_BYTE] == 0x08:
			logger.info('IOCON register OK. Returned data: {}'.format(rv))
			print(bcolors.BGRN+'IOCON OK'+bcolors.ENDC)
		else:
			logger.warn('IOCON register NOK! Returned data: {}'.format(rv))
			print(bcolors.BRED+'IOCON NOK'+bcolors.ENDC)
		# ---------------------------------------------------------------------

	def _set_pullup_for_gpioa(self, param):
		logger.info('Set pullup on Port A (bit 7-0)')
		self.spi.mode = SPI_MODE_0
		self.spi.xfer2([WRITE_OP_CODE, SPI_GPPUA, 0xff])

	def _set_pullup_for_gpiob(self, param):
		logger.info('Set pullup on Port B (bit 7-0)')
		self.spi.xfer2([WRITE_OP_CODE, SPI_GPPUB, 0xff])

	def _read_gpioa(self, param):
		self.spi.mode = SPI_MODE_0
		rv = self.spi.xfer2([READ_OP_CODE, SPI_GPIOA, DUMMY_BYTE])

		logger.info('Read SPI port A - CONTROL_BYTE: 0x{:02x}, reg: 0x{:02x} rv: 0x{:02x}'
		            .format(READ_OP_CODE, SPI_GPIOA, rv[SECOND_BYTE]))
		return rv

	def _read_gpiob(self, param):
		self.spi.mode = SPI_MODE_0
		rv = self.spi.xfer2([READ_OP_CODE, SPI_GPIOB, DUMMY_BYTE])

		logger.info('Read SPI port B - CONTROL_BYTE: 0x{:02x}, reg: 0x{:02x} rv: 0x{:02x}'
		            .format(READ_OP_CODE, SPI_GPIOB, rv[SECOND_BYTE]))
		return rv

	def get_dir_vectors(self):
		return self.port_A_dir_vector, self.port_B_dir_vector

	def get_pin_vectors(self):
		return self.port_A_pin_vector, self.port_B_pin_vector


# ------------------------------------------------------------------------------------------------------
# Test functions
# ------------------------------------------------------------------------------------------------------
def turn_on_off_5Ve_and_24Ve(mode):
	if mode == 1:
		print(bcolors.BRED+'Configure Port A and turn ON 5Ve and 24Ve'+bcolors.ENDC)
		port_write_cmd = 'i2cset -y 1 0x20 0x00 0xc0' # IODIRA
		os.system(port_write_cmd)
		time.sleep(0.1)
		port_write_cmd = 'i2cset -y 1 0x20 0x12 0x18' # GPIOA, 5Ve (R5)
		os.system(port_write_cmd)
		time.sleep(1)
	else:
		print(bcolors.BRED+'Turn OFF 5Ve'+bcolors.ENDC)
		port_write_cmd = 'i2cset -y 1 0x20 0x12 0x00' # GPIOA
		os.system(port_write_cmd)
		time.sleep(0.1)

def enable_spi0_CE0_3(enable):
	if enable == 1:
		print(bcolors.BYEL+'MCP23S17 - Enable CE3, CBA=011 and disable ext reset (RESET from U304)'+bcolors.ENDC)
		port_write_cmd = 'i2cset -y 1 0x20 0x01 0x21' # IODIRB
		os.system(port_write_cmd)
		port_write_cmd = 'i2cset -y 1 0x20 0x13 0x46' # GPIOB
		os.system(port_write_cmd)
		time.sleep(0.1)
	else:
		print('Disable CE3')
		port_write_cmd = 'i2cset -y 1 0x20 0x13 0x00'
		os.system(port_write_cmd)
		time.sleep(0.1)

def enable_spi0_CE0_4(enable):
	if enable == 1:
		print(bcolors.BYEL+'MCP23S17 - Enable CE4, CBA=100 and disable ext reset (RESET from U304)'+bcolors.ENDC)
		port_write_cmd = 'i2cset -y 1 0x20 0x01 0x21' # IODIRB
		os.system(port_write_cmd)
		port_write_cmd = 'i2cset -y 1 0x20 0x13 0x48' # GPIOB
		os.system(port_write_cmd)
		time.sleep(0.1)
	else:
		print('Disable CE4')
		port_write_cmd = 'i2cset -y 1 0x20 0x13 0x00'
		os.system(port_write_cmd)
		time.sleep(0.1)
# ---------------------------------------------------------------------------


def main():
	#turn_on_off_5Ve_and_24Ve(ON)
	myMCP = mcp23s17()
	time.sleep(4)

        # =========================================================
        # Below a number of test cases have been implemented.
        # To use them, comment/uncomment to select the test case
        # you want to run.
        # =========================================================

	#
	# U301 - inst 0, addr 0
	# ---------------------------------------------------------
	#enable_spi0_CE0_3(1)

	#mcpt.inst_0_addr_0_port_A7_test(myMCP) # U301
	#inst_0_addr_0_port_A0_test(myMCP) # U301
	#mcpt.inst_0_addr_0_port_B0_test(myMCP) # U301
	#mcpt.inst_0_addr_0_port_B7_test(myMCP) # U301
	# ---------------------------------------------------------

	#
	# U302 - inst 0, addr 1
	# 
	# ---------------------------------------------------------
	#enable_spi0_CE0_3(1)

	#mcpt.inst_0_addr_1_port_A7_test(myMCP) # U302
	#mcpt.inst_0_addr_1_port_A0_test(myMCP) # U302
	#mcpt.inst_0_addr_1_port_B0_test(myMCP) # U302
	#mcpt.inst_0_addr_1_port_B7_test(myMCP) # U302
	#mcpt.inst_0_addr_1_mux_test(myMCP) # Check MUX on It's-It
	# ---------------------------------------------------------

	#
	# U300 - inst 1, addr 1
	# 
	# ---------------------------------------------------------
	enable_spi0_CE0_4(1)

	#mcpt.inst_1_addr_0_port_A7_test(myMCP) # U300
	#mcpt.inst_1_addr_0_port_A0_test(myMCP) # U300
	#mcpt.inst_1_addr_0_port_B0_test(myMCP) # U300
	#mcpt.inst_1_addr_0_port_B7_test(myMCP) # U300

	mcpt.inst_1_addr_0_port_B_read(myMCP)
	# ---------------------------------------------------------

	time.sleep(DELAY_3s)
	#turn_on_off_5Ve_and_24Ve(OFF)

if __name__ == '__main__':
	main()
