# pylint: disable= line-too-long
# pylint: disable= too-many-branches
# pylint: disable= singleton-comparison

import logging
from robot.api import logger
from common_files.common import *
from common_files.common_dac61408 import *
import spidev
import time
import os

logging.basicConfig(level=logging.DEBUG)

DELIMITER = 70

SPI_PORT = 0
SPI_DEVICE = 0  # SPI1_CE0

_5V = 5.0
_m5V = -5.0
_10V = 10.0
_m10V = -10.0
_20V = 20.0
_m20V = -20.0
FULL_RANGE = 4095.0 # 12 bits, 0xfff is full range for DAC 
READ_ACCESS = 0x80

class bcolors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BYEL = '\033[1m' + '\033[93m'
    RED = '\033[91m'
    BRED = '\033[1m' + '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class dac61408:
	def __init__(self):
		self.spi = spidev.SpiDev()
		self.spi.open(SPI_PORT, SPI_DEVICE)
		self.spi.mode = SPI_MODE_2

		self.spi.max_speed_hz = SPI_LOW_SPEED
		logger.info('DAC init - SPI Mode: {} at speed: {} Hz'.format(self.spi.mode, self.spi.max_speed_hz))

		self.dispatcher = {DACRANGE0: self.config_dac, \
				   DACRANGE1: self.config_dac, \
		                   DAC0: self.dac_output, \
		                   DAC1: self.dac_output, \
		                   DAC2: self.dac_output, \
		                   DAC3: self.dac_output, \
		                   DAC4: self.dac_output, \
		                   DAC5: self.dac_output, \
		                   DAC6: self.dac_output, \
		                   DAC7: self.dac_output, \
		                   DEVICE_ID: self.get_device_id, \
		                   DAC_STATUS: self.get_status_info, \
		                   RAMP: self.ramp_output, \
		                   DACPWDWN: self.dac_power_down}

		self.dac_range_vector_A = 0x0000
		self.dac_range_vector_B = 0x0000
		self.power_down_vector = 0xffff

		self.dac_range = 0

	def configure(self, *params):
		reg = int(params[0]['Reg'], 16)
		rv = self.dispatcher[reg](params)
		return rv

	def _write_configuration(self, reg, vector):
			"""
			Serial interface access cycle

			|23|22|21|20|19|18|17|16|15|14|13|12|11|10| 9| 8| 7| 6| 5| 4| 3| 2| 1| 0|
			| 0| x|     reg.addr    |             Data in                           |

			"""
			vec0 = reg
			vec1 = (vector & 0xff00) >> 8
			vec2 = vector & 0x00ff
			logger.info('Vector: 0x{:02x}{:02x}{:02x} '.format(vec0, vec1, vec2))

			self.spi.mode = SPI_MODE_2
			self.spi.writebytes([vec0, vec1, vec2])

	def _get_range_prop(self, dac, dac_range):

		dac_no = dac - 0x14

		if dac_range == DAC_RANGE_0V_p5V:
			range_str = '0V to +5V'
		elif dac_range == DAC_RANGE_0V_p10V:
			range_str = '0V to +10V'
		elif dac_range == DAC_RANGE_m5V_p5V:
			range_str = '-5V to +5V'
		elif dac_range == DAC_RANGE_m10V_p10V:
			range_str = '-10V to +10V'
		elif dac_range == DAC_RANGE_m20V_p20V:
			range_str = '-20V to +20V'
		else:
			return 'None', 'None'

		return dac_no, range_str

	def ramp_output(self, params):
		logger.info('An example of creating a new function - Ramping voltage')
		return 'Voltage ramp'

	def config_dac(self, params):
		reg = int(params[0]['Reg'], 16)
		self.dac_range =  int(params[0]['Range'], 16)
		dac = int(params[0]['DAC'], 16)

		rv1, rv2 = self._get_range_prop(dac, self.dac_range)

		logger.info('Configuration of DAC - Register: 0x{:02x}, DAC: {}, Range: {}'.format(reg, rv1, rv2))

		# configure DAC0 - DAC3
		if reg == DACRANGE1 and dac < DAC4:
			if dac == DAC0:
				self.dac_range_vector_A |= (0x0f & self.dac_range)
				logger.info('DAC0 - range_vector: 0x{:04x}'.format(self.dac_range_vector_A))

			elif dac == DAC1:
				self.dac_range_vector_A |= (self.dac_range << 4)
				logger.info('DAC1 - range_vector: 0x{:04x}'.format(self.dac_range_vector_A))

			elif dac == DAC2:
				self.dac_range_vector_A |= (self.dac_range << 8)
				logger.info('DAC2 - range_vector: 0x{:04x}'.format(self.dac_range_vector_A))

			elif dac == DAC3:
				self.dac_range_vector_A |= (self.dac_range << 12)
				logger.info('DAC3 - range_vector: 0x{:04x}'.format(self.dac_range_vector_A))
			else:
				logger.warn('Invalid DAC for Range: {}'.format(reg))

			self._write_configuration(DACRANGE1, self.dac_range_vector_A)

		## configure DAC4 - DAC7
		elif reg == DACRANGE0 and dac > DAC3:
			if dac == DAC4:
				self.dac_range_vector_B |= (0x0f & self.dac_range)
				logger.info('DAC0 - range_vector: 0x{:04x}'.format(self.dac_range_vector_B))

			elif dac == DAC5:
				self.dac_range_vector_B |= (self.dac_range << 4)
				logger.info('DAC1 - range_vector: 0x{:04x}'.format(self.dac_range_vector_B))

			elif dac == DAC6:
				self.dac_range_vector_B |= (self.dac_range << 8)
				logger.info('DAC2 - range_vector: 0x{:04x}'.format(self.dac_range_vector_B))

			elif dac == DAC7:
				self.dac_range_vector_B |= (self.dac_range << 12)
				logger.info('DAC3 - range_vector: 0x{:04x}'.format(self.dac_range_vector_B))
			else:
				logger.warn('Invalid DAC for Range: {}'.format(reg))

			self._write_configuration(DACRANGE0, self.dac_range_vector_A)

		else:
			logger.warn('Invalid DAC range or combination range and DAC - Range: 0x{:02x}, DAC: 0x{:02x}'.format(reg, dac))

	def dac_power_down(self, params):
		reg =  int(params[0]['Reg'], 16)
		dac =  int(params[0]['DAC'], 16)
		mode =  params[0]['Mode']
		logger.info('Reg: {}, DAC: {}, Mode: {}'.format(reg, dac, mode))

		vec_normalized = dac - 0x14
		vec = 1 << (vec_normalized+4)  # bit 4 to bit 11 in register is used

		if mode == 'True':
			logger.info('Power Down DACs: {}'.format(mode))
			self.power_down_vector |= vec
			logger.info('Power down vec: {}'.format(self.power_down_vector))
			self._write_configuration(reg, self.power_down_vector)

		elif mode == 'False':
			logger.info('Power Up DACs: {}'.format(mode))
			self.power_down_vector &= ~vec
			logger.info('Power down vec: 0x{:02x}'.format(self.power_down_vector))
			self._write_configuration(reg, self.power_down_vector)

		else:
			logger.warn('Invalid mode: {}'.format(mode))

	def get_status_info(self, param):
		cmd = READ_ACCESS | DAC_STATUS

		self.spi.mode = SPI_MODE_2
		rv = self.spi.xfer2([cmd, PADDING_BYTE, PADDING_BYTE])
		time.sleep(DELAY_01s)
		rv = self.spi.xfer2([cmd, PADDING_BYTE, PADDING_BYTE])

		logger.info('Status: 0x{:02x}{:02x}{:02x}'.format(rv[0], rv[1], rv[2]))

	def get_device_id(self, param):
		# Since is not executed when object is instatiated from Robot Framework the
		# configuration is done here instead.
		# This means user have to call this before other configuration.
		logger.info('Configure SPI-/GENCONFIG and DACPWDWN')
		self.spi.xfer2([SPICONFIG, 0x0a, 0x84])  # Set device in Active Mode
		self.spi.xfer2([GENCONFIG, 0x00, 0x00])  # Activate internal reference
		self.spi.xfer2([DACPWDWN, 0x00, 0x00])   # Disable DAC power down mode

		# need to do 2 writing in order to get the id data, see data sheet DAC61408 p.28
		cmd = READ_ACCESS | DEVICE_ID

		self.spi.mode = SPI_MODE_2
		rv = self.spi.xfer5([cmd, PADDING_BYTE, PADDING_BYTE])
		time.sleep(DELAY_01s)
		rv = self.spi.xfer5([cmd, PADDING_BYTE, PADDING_BYTE])

		tmp = (rv[1] << 8) | rv[2]  
		device_id = (tmp & 0xfffc) >> 2
		logger.info('Returned value: {}, Device ID: 0x{:03x} - (shall be 0x248 for 12 bit version)'.format(rv, device_id))

		if device_id != 0x248:
			logger.warn('Incorrect Device ID from DAC61408')

	def dac_value(self, reg, value):
		"""
		Data format for a 12 bit DAC:

		DAC61408: {DATA[11:0], x, x, x, x}
		"""

		bit_19_16 = reg & 0x0f
		bit_23_20 = 0x01
		data1 = (bit_23_20 << 4) | bit_19_16

		bit_15_8 = (value & 0x0ff0) >> 4
		bit_7_0 = (value & 0x000f) << 4 | 0x0
		rv = [data1, bit_15_8, bit_7_0]

		return rv

	def check_input_parameters(self, voltage, dac_range):
		if dac_range == DAC_RANGE_0V_p5V:
			if (voltage < 0 or voltage > _5V):
				logger.warn('Incorrect voltage - voltage= {:.1f}'.format(voltage))
				return 0
			else:
				return 1

		elif dac_range == DAC_RANGE_0V_p10V:
			if (voltage < 0 or voltage > _10V):
				logger.warn('Incorrect voltage - voltage= {:.1f}'.format(voltage))
				return 0
			else:
				return 1

		elif dac_range == DAC_RANGE_0V_p20V:
			if (voltage < 0 or voltage > _20V):
				logger.warn('Incorrect voltage - voltage= {:.1f}'.format(voltage))
				return 0
			else:
				return 1

		elif dac_range == DAC_RANGE_m5V_p5V:
			if (voltage < _m5V or voltage > _5V):
				logger.warn('Incorrect voltage - voltage= {:.1f}'.format(voltage))
				return 0
			else:
				return 1

		elif dac_range == DAC_RANGE_m10V_p10V:
			if (voltage < _m10V or voltage > _10V):
				logger.warn('Incorrect voltage - voltage= {:.1f}'.format(voltage))
				return 0
			else:
				return 1

		elif dac_range == DAC_RANGE_m20V_p20V:
			if (voltage < _m20V or voltage > _20V):
				logger.warn('Incorrect voltage - voltage= {:.1f}'.format(voltage))
				return 0
			else:
				return 1
	
		else:
			logger.warn('Incorrect dac_range, DAC range: {}'.format(dac_range))
			return 0

	def calc_value(self, deltaX, voltage):
		deltaY = 2047
		k = deltaY / deltaX
		value = int(k * voltage + deltaY)
		logger.info('Calculated value (int/hex): {}, 0x{:03x}'.format(value, value))
		return value

	def dac_output(self, params):
		# These are just used for debugging
		#print('Params at dac_output:', params)
		#print('config_dac:', params)
		#print('Params:', params[0])
		#print('Device:', params[0]['Device'])
		#print('SPI-addr:', params[0]['SPI-addr'])
		#print(bcolors.BYEL+'Reg:', params[0]['Reg']+bcolors.ENDC)
		#print('Voltage', params[0]['Voltage'])

		value = 0
		voltage = float(params[0]['Voltage'])
		dac = int(params[0]['Reg'], 16)

		# [FIXME]: this should be checked that it is defined. Also check type so if statement is ok
		dac_range = self.dac_range
	
		if self.check_input_parameters(voltage, dac_range):
			if dac_range == DAC_RANGE_0V_p5V:
				logger.info('DAC range: 0 to 5V, voltage={:.1f}'.format(voltage))
				value = int(FULL_RANGE * voltage / _5V)
				logger.info('value: {}, 0x{:03x}'.format(value, value))
	
			elif dac_range == DAC_RANGE_0V_p10V:
				logger.info('DAC range: 0 to 10V, voltage={:.1f}'.format(voltage))
				value = int(FULL_RANGE * voltage / _10V)
				logger.info('value: {}, 0x{:03x}'.format(value, value))
	
			elif dac_range == DAC_RANGE_0V_p20V:
				logger.info('DAC range: 0 to 20V, voltage={:.1f}'.format(voltage))
				value = int(FULL_RANGE * voltage / _20V)
				logger.info('value: {}, 0x{:03x}'.format(value, value))
	
			elif dac_range == DAC_RANGE_m5V_p5V:
				logger.info('DAC range: -5V to +5V, voltage={:.1f}'.format(voltage))
				value = self.calc_value(_5V, voltage)
	
			elif dac_range == DAC_RANGE_m10V_p10V:
				logger.info('DAC range: -10V to +10V, voltage={:.1f}'.format(voltage))
				value = self.calc_value(_10V, voltage)
	
			elif dac_range == DAC_RANGE_m20V_p20V:
				logger.info('DAC range: -20V to +20V, voltage={:.1f}'.format(voltage))
				value = self.calc_value(_20V, voltage)
	
			rv = self.dac_value(dac, value)
			logger.info('DAC data = 0x{:02x}{:02x}{:02x} for DAC: {}'
	                      .format(rv[0], rv[1], rv[2], dac-DAC0))

			self.spi.mode = SPI_MODE_2
			self.spi.xfer2([rv[0], rv[1], rv[2]])
	
		else:
			logger.warn('Voltage/DAC range check failed')

	def close_port(self):
		logger.info('SPI port is closed')
		self.spi.close()


# --------------------------------------------------------------------------------
# Test purpose functions
# --------------------------------------------------------------------------------
def turn_on_off_5Ve(mode):
	if mode == 1:
		print(bcolors.BRED+'Configure Port A and turn ON 5Ve'+bcolors.ENDC)
		port_write_cmd = 'i2cset -y 1 0x20 0x00 0xc0' # IODIRA
		os.system(port_write_cmd)
		time.sleep(0.1)
		port_write_cmd = 'i2cset -y 1 0x20 0x12 0x10' # GPIOA, 5Ve (R5)
		os.system(port_write_cmd)
		time.sleep(1)
	else:
		print(bcolors.BRED+'Turn OFF 5Ve'+bcolors.ENDC)
		port_write_cmd = 'i2cset -y 1 0x20 0x12 0x00' # GPIOA
		os.system(port_write_cmd)
		time.sleep(0.1)

def enable_spi0_CE0_0(enable):
	if enable == 1:
		print(bcolors.BYEL+'DAC61408 - Enable CE0, CBA=000 and disable ext reset (RESET from U304)'+bcolors.ENDC)
		port_write_cmd = 'i2cset -y 1 0x20 0x01 0x21' # IODIRB
		os.system(port_write_cmd)
		port_write_cmd = 'i2cset -y 1 0x20 0x13 0x40' # GPIOB
		os.system(port_write_cmd)
		time.sleep(0.1)
	else:
		print(bcolors.BRED+'Disable CE0'+bcolors.ENDC)
		port_write_cmd = 'i2cset -y 1 0x20 0x13 0x00'
		os.system(port_write_cmd)
		time.sleep(0.1)

def get_devid(obj):
	obj.get_device_id(DUMMY_BYTE)

def get_status(obj):
	obj.get_status_info(DUMMY_BYTE)

def dac0_0_5V_test_1(obj):
	print(bcolors.BYEL+'DAC1 test - Output=3.0 V - U408:6'+bcolors.ENDC)
	_DACRANGE1 = '0x0c'
	_DAC_RANGE_0V_p5V = '0x0'
	_DAC0 = '0x14'
	item = {'Device':DAC61408_DEVICE, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_DACRANGE1, 'Range':_DAC_RANGE_0V_p5V, 'DAC': _DAC0}
	obj.configure(item)

	time.sleep(DELAY_05s)

	item2 = {'Device':DAC61408_DEVICE, 'SPI-addr':SPI_ADDRESS_0, 'Reg':'0x14', 'Voltage':'3.0'}
	obj.configure(item2) 

	print(DELIMITER*'-')

def dac0_0_10V_test_1(obj):
	print(bcolors.BYEL+'DAC1 test - U408:6'+bcolors.ENDC)
	_DACRANGE1 = '0x0c'
	_DAC_RANGE_0V_p10V = '0x1'
	_DAC0 = '0x14'
	item = {'Device':DAC61408_DEVICE, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_DACRANGE1, 'Range':_DAC_RANGE_0V_p10V, 'DAC': _DAC0}
	obj.configure(item)

	time.sleep(DELAY_05s)

	item2 = {'Device':DAC61408_DEVICE, 'SPI-addr':SPI_ADDRESS_0, 'Reg':'0x14', 'Voltage':'8.0'}
	obj.configure(item2) 

	print(DELIMITER*'-')

def dac1_0_5V_test_1(obj):
	print(bcolors.BYEL+'DAC1 test - Output=3.1 V - U408:6'+bcolors.ENDC)
	_DACRANGE1 = '0x0c'
	_DAC_RANGE_0V_p5V = '0x0'
	_DAC1 = '0x15'
	item = {'Device':DAC61408_DEVICE, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_DACRANGE1, 'Range':_DAC_RANGE_0V_p5V, 'DAC': _DAC1}
	obj.configure(item)

	time.sleep(DELAY_05s)

	item2 = {'Device':DAC61408_DEVICE, 'SPI-addr':SPI_ADDRESS_0, 'Reg':'0x15', 'Voltage':'3.1'}
	obj.configure(item2) 

	print(DELIMITER*'-')

def dac1_0_5V_test_2(obj):
	print(bcolors.BYEL+'DAC1 test - Output=0 V - U408:6'+bcolors.ENDC)
	_DACRANGE1 = '0x0c'
	_DAC_RANGE_0V_p5V = '0x0'
	_DAC1 = '0x15'
	item = {'Device':DAC61408_DEVICE, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_DACRANGE1, 'Range':_DAC_RANGE_0V_p5V, 'DAC': _DAC1}
	obj.configure(item)

	time.sleep(DELAY_05s)

	item2 = {'Device':DAC61408_DEVICE, 'SPI-addr':SPI_ADDRESS_0, 'Reg':'0x15', 'Voltage':'0'}
	obj.configure(item2) 

	print(DELIMITER*'-')

def dac1_0_5V_test_3(obj):
	print(bcolors.BYEL+'DAC1 test - Output=4 V - U408:6'+bcolors.ENDC)
	_DACRANGE1 = '0x0c'
	_DAC_RANGE_0V_p5V = '0x0'
	_DAC1 = '0x15'
	item = {'Device':DAC61408_DEVICE, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_DACRANGE1, 'Range':_DAC_RANGE_0V_p5V, 'DAC': _DAC1}
	obj.configure(item)

	time.sleep(DELAY_05s)

	item2 = {'Device':DAC61408_DEVICE, 'SPI-addr':SPI_ADDRESS_0, 'Reg':'0x15', 'Voltage':'2.0'}
	obj.configure(item2) 

	print(DELIMITER*'-')

def dac1_0_10V_test_1(obj):
	print(bcolors.BYEL+'DAC1 test - Output=7.5 V - U408:6'+bcolors.ENDC)
	_DACRANGE1 = '0x0c'
	_DAC_RANGE_0V_p10V = '0x1'
	_DAC1 = '0x15'
	item = {'Device':DAC61408_DEVICE, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_DACRANGE1, 'Range':_DAC_RANGE_0V_p10V, 'DAC': _DAC1}
	obj.configure(item)

	time.sleep(DELAY_05s)

	item2 = {'Device':DAC61408_DEVICE, 'SPI-addr':SPI_ADDRESS_0, 'Reg':'0x15', 'Voltage':'7.5'}
	obj.configure(item2) 

	print(DELIMITER*'-')

def dac1_0_10V_test_2(obj):
	print(bcolors.BYEL+'DAC1 test - Output=3 V - U408:6'+bcolors.ENDC)
	_DACRANGE1 = '0x0c'
	_DAC_RANGE_0V_p10V = '0x1'
	_DAC1 = '0x15'
	item = {'Device':DAC61408_DEVICE, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_DACRANGE1, 'Range':_DAC_RANGE_0V_p10V, 'DAC': _DAC1}
	obj.configure(item)

	time.sleep(DELAY_05s)

	item2 = {'Device':DAC61408_DEVICE, 'SPI-addr':SPI_ADDRESS_0, 'Reg':'0x15', 'Voltage':'3.0'}
	obj.configure(item2) 

	print(DELIMITER*'-')

def dac1_0_20V_test_1(obj):
	print(bcolors.BYEL+'DAC1 test - Output=15.1 V - U408:6'+bcolors.ENDC)
	_DACRANGE1 = '0x0c'
	_DAC_RANGE_0V_p20V = '0x2'
	_DAC1 = '0x15'
	item = {'Device':DAC61408_DEVICE, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_DACRANGE1, 'Range':_DAC_RANGE_0V_p20V, 'DAC': _DAC1}
	obj.configure(item)

	time.sleep(DELAY_05s)

	item2 = {'Device':DAC61408_DEVICE, 'SPI-addr':SPI_ADDRESS_0, 'Reg':'0x15', 'Voltage':'15.1'}
	obj.configure(item2) 

	print(DELIMITER*'-')

def dac1_power_down_test(obj):
	_DACRANGE1 = '0x0c'
	_DAC_RANGE_0V_p20V = '0x2'
	_DAC1 = '0x15'
	item = {'Device':DAC61408_DEVICE, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_DACRANGE1, 'Range':_DAC_RANGE_0V_p20V, 'DAC': _DAC1}
	obj.configure(item)
	time.sleep(1)

	item2 = {'Device':DAC61408_DEVICE, 'SPI-addr':SPI_ADDRESS_0, 'Reg':'0x15', 'Voltage':'15.1'}
	obj.configure(item2) 
	time.sleep(2)

	_DACPWDWN = '0x09'
	item3 = {'Device':DAC61408_DEVICE, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_DACPWDWN, 'DAC': _DAC1, 'Mode': 'True'}
	obj.configure(item3)

def main():
	#turn_on_off_5Ve(ON)
	#time.sleep(DELAY_05s)

	enable_spi0_CE0_0(1)

	myDAC = dac61408()

	# =========================================================
	# Below a number of test cases have been implemented.
	# To use them, comment/uncomment to select the test case
	# you want to run.
	# =========================================================

	# ---------------------------------------------------
	get_devid(myDAC)
	get_status(myDAC)
	#print(DELIMITER*'-')
	# ---------------------------------------------------

	# ---------------------------------------------------
	# DAC test 0-5 V
	#dac0_0_5V_test_1(myDAC)
	dac0_0_10V_test_1(myDAC)

	# ---------------------------------------------------
	# DAC test 0-5 V
	#dac1_0_5V_test_1(myDAC)
	#time.sleep(DELAY_2s)
	#dac1_0_5V_test_2(myDAC)
	#time.sleep(DELAY_2s)
	#dac1_0_5V_test_3(myDAC)
	# ---------------------------------------------------

	# ---------------------------------------------------
	# DAC test 0-10 V
	#dac1_0_10V_test_1(myDAC)
	#time.sleep(DELAY_2s)
	#dac1_0_10V_test_2(myDAC)
	# ---------------------------------------------------

	# ---------------------------------------------------
	# DAC test 0-20 V
	#dac1_0_20V_test_1(myDAC)
	# ---------------------------------------------------

	# ---------------------------------------------------
	# DAC power down test
	#dac1_power_down_test(myDAC)
	# ---------------------------------------------------

	time.sleep(DELAY_3s)
	#turn_on_off_5Ve(OFF)


if __name__ == '__main__':
	main()
