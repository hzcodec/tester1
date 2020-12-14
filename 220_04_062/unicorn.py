# pylint: disable=pointless-statement
# pylint: disable=protected-access

#import logging
import time

from robot.api import logger

import ad4112
import CANopen
import dac61408
import mcp23017
import mcp23s17
import os
import unicorn_test_cases as utc

from common_files.common import *
from common_files.common_mcp23017 import *
from common_files.common_mcp23s17 import *
from common_files.common_ad4112 import *
from common_files.common_dac61408 import *

# library used during development
from config import MCP1, MCP2, AD1

OFFSET_OF_BIT = 8
DELIMITER = 60
SPACE = 20

PORT_OFFSET_8 = 8    # used to offset port number to 0
PORT_OFFSET_16 = 16  #            -"-
PORT_OFFSET_24 = 24  #            -"-
PORT_OFFSET_31 = 31  #            -"-
PORT_OFFSET_40 = 40  #            -"-


class bcolors:
    GREEN = '\033[92m'
    BGREEN = '\033[1m' + '\033[92m'
    RED = '\033[91m'
    BRED = '\033[1m' + '\033[91m'
    YELLOW = '\033[93m'
    BYEL = '\033[1m' + '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class unicorn:
	ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

	def __init__(self):
		logger.info('Create instances of all components')
		self.io_expander_1_i2c = mcp23017.mcp23017(MCP23017_ADDR_0)
		self.io_expander_2_i2c = mcp23017.mcp23017(MCP23017_ADDR_1)
		self.adc1 = ad4112.ad4112()

		self.CANopen = CANopen.CANopen()
		# [FIXME]: This is'nt created for some reason. Done in init_dac() instead.
		#self.dac = dac61408.dac61408()

		self.config_locked_by_system = False

	# ------------------------------------------------------------
	# MCP23017
	# ------------------------------------------------------------
	def init_io_expander_i2c(self):
		"""
		Port GPA0 - GPA5 are outputs
		Port GPA6 - GPA7 are inputs

		Port GPB0        is input
		Port GPB1 - GPB4 are outputs
		Port GPB5        is input
		Port GPB6 - GPB7 are outputs
		"""
		logger.info(DELIMITER*'-')
		logger.info('Initialize 16-bit I/O Expander, I2C - MCP23017, addr=0')

		#
		# N.B! default mode for a port is 'IN', therefore this is not configured.
		#
		logger.info(SPACE*' '+'--- Port A ---, GPA0-5 out')
		for port in range(I2C_GPA0, I2C_GPA5+1):
			self.io_expander_1_i2c.configure(I2C_IODIRA, port, OUT)

		logger.info(SPACE*' '+'--- Port B ---, GPB1-4 and GPB6-7 out')
		for port in range(I2C_GPB1, I2C_GPB4+1):
			self.io_expander_1_i2c.configure(I2C_IODIRB, port, OUT)

		self.io_expander_1_i2c.configure(I2C_IODIRB, I2C_GPB6, OUT)
		self.io_expander_1_i2c.configure(I2C_IODIRB, I2C_GPB7, OUT)

		self.io_expander_1_i2c.configure(I2C_GPIOB, I2C_GPB6, HIGH) # RESET for SPI components, active low

		""" 
		Port GPA0 - GPA7 are outputs
		Port GPB0 - GPB7 are outputs
		"""
		logger.info(DELIMITER*'-')
		logger.info('Initialize 16-bit I/O Expander, I2C - MCP23017, addr=1')
		logger.info(SPACE*' '+'--- Port A/B --- out')
		self._config_io_port_A_and_B()

	def power_control(self, relay, mode):
		if int(mode) == ON:
			self.io_expander_1_i2c.configure(I2C_GPIOA, int(relay), HIGH)
		else:
			self.io_expander_1_i2c.configure(I2C_GPIOA, int(relay), LOW)

		logger.info('Power control: Power: {}, mode: {}'.
		             format(mcp23017_get_power_name(int(relay)), mcp23017_get_level_name(int(mode))))

		time.sleep(DELAY_05s)

	def relay_control(self, relay, mode):
		"""
		Control the relays connected to MCP23017, addr=1
		"""
		logger.info('Relay: {} Level: {}'.format(int(relay)+1, mcp23017_get_level_name(int(mode))))

		if int(relay) < 8:
			if int(mode) == ON:
				self.io_expander_2_i2c.configure(I2C_GPIOA, int(relay), HIGH)
			else:
				self.io_expander_2_i2c.configure(I2C_GPIOA, int(relay), LOW)

		elif int(relay) < 17:
			if int(mode) == ON:
				self.io_expander_2_i2c.configure(I2C_GPIOB, int(relay)-OFFSET_OF_BIT, HIGH)
			else:
				self.io_expander_2_i2c.configure(I2C_GPIOB, int(relay)-OFFSET_OF_BIT, LOW)

		else:
			logger.warn('Invalid Relay: {}'.format(relay))

		time.sleep(DELAY_02s)

	def read_closed(self):
		closed = 0x00
		closed = self.io_expander_1_i2c.configure(I2C_READ_PORT_A)

		if (closed & 0x80):
			logger.info('Lid is closed')
			return 1
		else:
			logger.info('Lid is open')
			return 0

	def read_s3(self):
		s3 = 0x00
		s3 = self.io_expander_1_i2c.configure(I2C_READ_PORT_B)

		if (s3 & 0x01):
			logger.info('S3 high')
			return 1
		else:
			logger.info('S3 low')
			return 0

	def spi0_ce0(self, device, en):
		logger.info('SPI0_CE0_{} enable: {} and disable RESET for Device: {}'.format(device, en, device))

		bit0 = device & (1 << 0)
		bit1 = (device & (1 << 1)) >> 1
		bit2 = (device & (1 << 2)) >> 2

		if en == 1:
			#logger.info('Enable CS for device: {}'.format(mcp23017_get_device_name(device)))
			logger.info('Enable CS for device: {}'.format(device))
			self.io_expander_1_i2c.configure(I2C_GPIOB, I2C_GPB1, bit0) # A0 to address decoder
			self.io_expander_1_i2c.configure(I2C_GPIOB, I2C_GPB2, bit1) # A1       -"-
			self.io_expander_1_i2c.configure(I2C_GPIOB, I2C_GPB3, bit2) # A2       -"-
		else:
			self.io_expander_1_i2c.configure(I2C_GPIOB, I2C_GPB1, LOW)
			self.io_expander_1_i2c.configure(I2C_GPIOB, I2C_GPB2, LOW)
			self.io_expander_1_i2c.configure(I2C_GPIOB, I2C_GPB3, LOW)

	def set_safe(self, mode):
		if int(mode) == ON:
			self.io_expander_1_i2c.configure(I2C_GPIOB, I2C_GPA3, HIGH)
			logger.info('Lock lid')
		else:
			self.io_expander_1_i2c.configure(I2C_GPIOB, I2C_GPA3, LOW)
			logger.info('Unlock lid')

	def set_reset(self, mode):
		if int(mode) == ON:
			self.io_expander_1_i2c.configure(I2C_GPIOB, I2C_GPA4, LOW)
			logger.info('Set Reset')
		else:
			self.io_expander_1_i2c.configure(I2C_GPIOB, I2C_GPA4, HIGH)
			logger.info('Release Reset')

	# ........................................................................
	# Handling of addr=0x21, all 16 ports are controlling the relays
	def _config_io_port_A_and_B(self):
		for port in range(I2C_GPA0, I2C_GPA7+1):
			self.io_expander_2_i2c.configure(I2C_IODIRA, port, OUT)

		for port in range(I2C_GPB0, I2C_GPB7+1):
			self.io_expander_2_i2c.configure(I2C_IODIRB, port, OUT)

	# ........................................................................

	# ------------------------------------------------------------
	# MCP23S17
	# ------------------------------------------------------------
	def init_io_expander_spi(self):
		logger.info('Initialize 16-bit I/O Expander, SPI - MCP23S17')
		self.io_expander_spi = mcp23s17.mcp23s17()

	def set_config_lock(self):
		self.config_locked_by_system = True

	def config_mcp(self, item):
		logger.info('Config MCP23S17: {}'.format(item))

		device = int(item["Device"])
		address = int(item["SPI-addr"])
		reg = int(item["Reg"], 16)

		#logger.info('Device: {}, Addr: {}, Reg: {}'.format(device, address, reg))

		self.spi0_ce0(device, 1)
		time.sleep(DELAY_02s)

		rv = self.io_expander_spi.configure(item)
		time.sleep(DELAY_02s)
		return rv

	def config_mcp_port(self, port, mode):
		logger.info('Port: {}, Mode: {}'.format(port, mode))

		_MCP23S17_DEVICE_0 = '3'
		_MCP23S17_DEVICE_1 = '4'
		_MCP23S17_ADDR_0 = '0'
		_MCP23S17_ADDR_1 = '1'
		_SPI_IODIRA = '0x00'
		_SPI_IODIRB = '0x01'

		if int(port) >= 0 and int(port) <= 7:
			logger.info('Dev 0, Addr 0, Port A')
			item = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_IODIRA, 'Port':port, 'Mode':mode}

		elif int(port) > 7 and int(port) <= 15:
			logger.info('Dev 0, Addr 0, Port B')
			_port = str(int(port) - PORT_OFFSET_8)
			item = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_IODIRB, 'Port':_port, 'Mode':mode}

		elif int(port) > 15 and int(port) <= 23:
			logger.info('Dev 0, Addr 1, Port A')
			_port = str(int(port) - PORT_OFFSET_16)
			item = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_IODIRA, 'Port':_port, 'Mode':mode}

		elif int(port) > 23 and int(port) <= 31:
			logger.info('Dev 0, Addr 1, Port B')
			_port = str(int(port) - PORT_OFFSET_24)
			item = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_IODIRB, 'Port':_port, 'Mode':mode}

		elif int(port) > 31 and int(port) <= 39:
			logger.info('Dev 1, Addr 0, Port A')
			_port = str(int(port) - PORT_OFFSET_31)
			item = {'Device':_MCP23S17_DEVICE_1, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_IODIRA, 'Port':_port, 'Mode':mode}

		elif int(port) > 39 and int(port) <= 47 and not self.config_locked_by_system:
			_port = str(int(port) - PORT_OFFSET_40)
			logger.info('Dev 1, Addr 0, Port B, {}'.format(_port))
			item = {'Device':_MCP23S17_DEVICE_1, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_IODIRB, 'Port':_port, 'Mode':mode}

		else:
			logger.error('Illegal SPI MCP I/O port declaration, port: {}'.format(port))

		self.config_mcp(item)

	def set_mcp_port(self, port, level):
		logger.info('Port: {}, Level: {}'.format(port, level))

		_MCP23S17_DEVICE_0 = '3'
		_MCP23S17_ADDR_0 = '0'
		_MCP23S17_ADDR_1 = '1'
		_SPI_GPIOA = '0x12'
		_SPI_GPIOB = '0x13'

		# DIO-7 - DIO-0
		if int(port) >= 0 and int(port) <= 7:
			item = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_GPIOA, 'Port':port, 'Mode':level}

		# DIO-15 - DIO-8
		elif int(port) > 7 and int(port) <= 15:
			logger.info('Dev 0, Addr 0, Port B: {}'.format(port))
			_port = str(int(port) - PORT_OFFSET_8)
			item = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_GPIOB, 'Port':_port, 'Mode':level}

		# DIO-23 - DIO-16
		elif int(port) > 15 and int(port) <= 23:
			_port = str(int(port) - PORT_OFFSET_16)
			item = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_GPIOA, 'Port':_port, 'Mode':level}

		# GPIO7_C - GPIO0_C
		elif int(port) > 23 and int(port) <= 31:
			_port = str(int(port) - PORT_OFFSET_24)
			item = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_GPIOB, 'Port':_port, 'Mode':level}

		else:
			logger.warn('Illegal port declaration when port is written')

		self.config_mcp(item)

	def set_gpbc_port(self, data):
		_MCP23S17_DEVICE_0 = '3'
		_MCP23S17_ADDR_1 = '1'

		item = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':hex(SPI_GPB_C), 'Data': data}
		self.config_mcp(item)
		
	
	def read_mcp_port(self, port):
		str_read_a = str(hex(SPI_READ_A))
		str_read_b = str(hex(SPI_READ_B))

		_MCP23S17_DEVICE_1 = '4'
		_MCP23S17_ADDR_0 = '0'

		if port == str_read_a:
			logger.info('Read MCP23S17 port A')
			item = {'Device':_MCP23S17_DEVICE_1, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':hex(SPI_READ_A)}

		elif port == str_read_b:
			logger.info('Read MCP23S17 port B')
			item = {'Device':_MCP23S17_DEVICE_1, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':hex(SPI_READ_B)}

		else:
			logger.warn('Illegal port declaration when port is read')

		rv = self.config_mcp(item)
		return rv

	# ------------------------------------------------------------
	# AD4112
	# ------------------------------------------------------------
	def init_adc(self):
		logger.info('Initialize 8 channel ADC, SPI - AD4112')

	def config_adc(self, item):
		logger.info('Item: {}'.format(item))

		device = int(item["Device"])
		#address = int(item["SPI-addr"])
		#reg = item["Reg"]

		self.spi0_ce0(device, 1)
		rv = self.adc1.configure(item)
		return rv

	# ------------------------------------------------------------
	# DAC61416, 16 ch, 12 bit DAC
	# ------------------------------------------------------------
	def init_dac(self):
		logger.info('Initialize DAC, SPI - DAC61416')
		self.dac = dac61408.dac61408()

	def enable_spi0_CE0_0(self):
		logger.info('DAC61408 - Enable CE0')
		port_write_cmd = 'i2cset -y 1 0x20 0x01 0x21' # IODIRB
		os.system(port_write_cmd)
		port_write_cmd = 'i2cset -y 1 0x20 0x13 0x40' # GPIOB
		os.system(port_write_cmd)
		time.sleep(0.1)

	def config_dac(self, item):
		logger.info('Config2 DAC Item: {}'.format(item))

		device = int(item["Device"])
		address = int(item["SPI-addr"])

		# [FIXME]: For some reason a call to 'spi0_ce0(self, device, en)' does not work.
		#          Using a another function for cs-handling.
		#	   This is a fix for the DAC.
		#self.enable_spi0_CE0_0()
		self.spi0_ce0(device, 1)
		self.dac.configure(item)
		#self.spi0_ce0(5, 0)

	def config_dac2(self, item):
		logger.info('Config DAC2 Item: {}'.format(item))

		device = int(item["Device"])
		address = int(item["SPI-addr"])
		rv = self.dac.configure(item)
		logger.info('Handle result here in config_dac2: {}'.format(rv))


def main():

	myUnicorn = unicorn()


if __name__ == '__main__':
	main()
