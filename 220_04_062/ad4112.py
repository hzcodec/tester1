import logging
import os
import time
import sys
from robot.api import logger
from common_files.common import *
import spidev

logging.basicConfig(level=logging.DEBUG)

SPI_PORT = 0
SPI_DEVICE = 0  # SPI1_CE0
DELIMITER = 90

MAX_IN_VOLT = 10    # V
MAX_CURRENT = 20.0  # mA


class bcolors:
    GREEN = '\033[92m'
    BGREEN = '\033[1m' + '\033[92m'
    RED = '\033[91m'
    BRED = '\033[1m' + '\033[91m'
    YELLOW = '\033[93m'
    BYEL = '\033[1m' + '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class ad4112:
	"""
	12-bit ADC.
	According to the datasheet AD7490 requires CS as framing signal
	for every 16 bit read or write transaction.

	1) After a power-up cycle and when the power supplies are stable,
	   a device reset is required

	2) All communication begins by writing to the communications register.

	Writing to register:
	
	   8-bit command               8/16/24 bits of data             8-bit CRC
	|<--------------->|<--------------------------------------->|<------------->|
	"""

	_inst_counter = 0

	def __init__(self):
		self.spi = spidev.SpiDev()
		self.spi.open(SPI_PORT, SPI_DEVICE)
		self.spi.max_speed_hz = SPI_LOW_SPEED
		self.spi.mode = SPI_MODE_3
		self.gp_vector = 0x00

		self.dispatcher = {ID: self.get_id, \
		                   GPIOCON: self.set_gpio, \
		                   CH0: self.config_channel, \
		                   CH1: self.config_channel, \
		                   CH2: self.config_channel, \
		                   CH3: self.config_channel, \
		                   CH4: self.config_channel, \
		                   CH5: self.config_channel, \
		                   CH6: self.config_channel, \
		                   CH7: self.config_channel, \
		                   STATUS: self.get_status, \
		                   SETUPCON0: self.config_setup_0, \
		                   SETUPCON1: self.config_setup_1, \
		                   ADCMODE: self.config_adc_mode, \
		                   IFMODE: self.config_interface_mode, \
		                   DATA: self.get_data}
		ad4112._inst_counter += 1
		self.id = ad4112._inst_counter

	def configure(self, *params):
		#logger.info('ADC4112 Inst counter: {}'.format(self.id))
		reg = int(params[0]['Reg'], 16)
		rv = self.dispatcher[reg](params)
		return rv

	def _config_ad(self):
		logger.info('Configure AD4112')
	
	def device_reset(self):
		"""
		64 serial clock cycles with DIN high => sets ADC to default state
		"""
		logger.info('Device Reset')
		self.spi.writebytes([0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff])
		print(DELIMITER*'-')

	def config_channel(self, param):
		selected_register = int(param[0]['Reg'], 16)
		logger.info('Configure channel: {}'.format(selected_register-16))

		if selected_register == CH0:
			vec = CH_EN | SETUP_SEL_0 | INPUT_VIN0
			self.config_channel_reg(CH0, vec)

		elif selected_register == CH1:
			vec = CH_EN | SETUP_SEL_0 | INPUT_VIN1
			self.config_channel_reg(CH1, vec)

		elif selected_register == CH2:
			vec = CH_EN | SETUP_SEL_0 | INPUT_VIN2
			self.config_channel_reg(CH2, vec)

		elif selected_register == CH3:
			vec = CH_EN | SETUP_SEL_0 | INPUT_VIN3
			self.config_channel_reg(CH3, vec)

		elif selected_register == CH4:
			vec = CH_EN | SETUP_SEL_0 | INPUT_VIN4
			self.config_channel_reg(CH4, vec)

		elif selected_register == CH5:
			vec = CH_EN | SETUP_SEL_0 | INPUT_VIN5
			self.config_channel_reg(CH5, vec)

		elif selected_register == CH6:
			vec = CH_EN | SETUP_SEL_0 | INPUT_VIN6
			self.config_channel_reg(CH6, vec)

		elif selected_register == CH7:
			vec = CH_EN | SETUP_SEL_0 | INPUT_VIN7
			self.config_channel_reg(CH7, vec)

		else:
			logger.info('Incorrect channel selected')

	def get_id(self, param):
		self.device_reset()

		command = 0x00 | RD | ID
		logger.info('Get ID - command: 0x{:02x}'.format(command))

		self.spi.mode = SPI_MODE_3
		rv = self.spi.xfer4([command, PADDING_BYTE, PADDING_BYTE])
		product_id = rv[1] << 4 | (rv[2] >> 4)

		logger.info("Product ID: Got 0x{:03x} (Expected 0x30dx, x=don't care')".format(product_id))
		if product_id != 781:  # = 0x30d
			logger.error('Product ID does not match!')

		self.update_gain(GAIN0, [0xd5, 0x97, 0xda])
		self.update_gain(GAIN1, [0xd5, 0x97, 0xda])

		return product_id

	def set_gpio(self, param):
		command = 0x00 | GPIOCON 
		byte1 = 0x20 # enable GPIO0 and GPIO1 as output signals
		mode = param[0]['Mode']
		gpio = int(param[0]['GP'], 16)

		if mode == '1':
			self.gp_vector |= gpio 
		else:
			self.gp_vector &= ~(gpio)

		byte2 = self.gp_vector

		logger.info('Set GP - command: 0x{:02x} 0x{:02x} 0x{:02x}'.format(command, byte1, byte2))
		self.spi.mode = SPI_MODE_3
		self.spi.xfer2([command, byte1, byte2])

	def update_offset(self, reg, val):
		command = 0x00 | reg
		logger.info('Update OFFSET{} - command: 0x{:02x} 0x{:02x} 0x{:02x} 0x{:02x}'.format(reg-48, command, val[0], val[1], val[2]))
		self.spi.mode = SPI_MODE_3
		self.spi.xfer2([command, val[0], val[1], val[2]])

	def update_gain(self, reg, val):
		command = 0x00 | reg
		logger.info('Update GAIN{} - command: 0x{:02x} 0x{:02x} 0x{:02x} 0x{:02x}'.format(reg-56, command, val[0], val[1], val[2]))
		self.spi.mode = SPI_MODE_3
		self.spi.xfer2([command, val[0], val[1], val[2]])

	def config_channel_reg(self, reg, vec):
		if reg < CH0 or reg > CH15:
			logger.warn('Invalid channel: {}'.format(reg))
		else:
			reg_masked = reg & 0x0f
			command = 0x00 | reg

			byte1 = (vec & 0xff00) >> 8
			byte2 = vec & 0x00ff

			setup_sel = vec & 0x7000
			rv = ad4112_get_setup_name(setup_sel)

			input_n = vec & 0x3ff
			rv2 = ad4112_get_input_name(input_n)

			logger.info('Configure channel (reg: 0x{:02x}), CH{} with {}/{} - command: 0x{:02x} 0x{:02x} 0x{:02x}'.
			            format(reg, reg_masked, rv2, rv, command, byte1, byte2))

			self.spi.mode = SPI_MODE_3
			self.spi.xfer2([command, byte1, byte2])

	def config_adc_mode(self, vec):
		command = 0x00 | ADCMODE 
		vec = REF_EN | SING_SYNC | SING_CONV

		adc_mode = vec & 0x70
		rv = ad4112_get_adc_mode_name(adc_mode)

		# bit[13] SING_SYNC, enabled
		byte1 = (0xff00 & vec) >> 8

		# bit[6:4] Mode, 000=Cont conv, 001=Single conv
		byte2 = adc_mode

		logger.info('Configure ADC mode (reg: 0x01) with {} - command: 0x{:02x} 0x{:02x} 0x{:02x}'.format(rv, command, byte1, byte2))
		self.spi.mode = SPI_MODE_3
		self.spi.xfer2([command, byte1, byte2])

	def config_interface_mode(self, vec):
		command = 0x00 | IFMODE 
		byte1 = 0x00
		vec = DATA_STAT

		# bit[6] DATA_STAT enabled
		# bit[0] WL16, 0=24-bit, 1=16-bit data
		byte2 = vec

		rv = ad4112_get_stat_name(vec)

		logger.info('Configure Interface mode (reg: 0x02) with {} - command: 0x{:02x} 0x{:02x} 0x{:02x}'.format(rv, command, byte1, byte2))
		self.spi.mode = SPI_MODE_3
		self.spi.xfer2([command, byte1, byte2])

	def config_setup_0(self, param):
		logger.info('Input param: {}'.format(param))

		BI_UNI_POLAR = param[0]['Type']
		BI_UNI_POLAR_int = int(BI_UNI_POLAR, 16)
		vec = BI_UNI_POLAR_int | REF_BUFP | REF_BUFM | INBUF_EN

		command = 0x00 | SETUPCON0
		byte1 = (0xff00 & vec) >> 8
		byte2 = 0x00ff & vec

		logger.info('Configure Setup 0 (reg: 0x20) - command: 0x{:02x} 0x{:02x} 0x{:02x}'.format(command, byte1, byte2))
		self.spi.mode = SPI_MODE_3
		self.spi.xfer2([command, byte1, byte2])

	def config_setup_1(self, param):
		logger.info('Input param: {}'.format(param))

		BI_UNI_POLAR = param[0]['Type']
		BI_UNI_POLAR_int = int(BI_UNI_POLAR, 16)
		vec = BI_UNI_POLAR_int | REF_BUFP | REF_BUFM | INBUF_EN

		vec = REF_BUFP | REF_BUFM | INBUF_EN

		command = 0x00 | SETUPCON1
		byte1 = (0xff00 & vec) >> 8
		byte2 = 0x00ff & vec

		logger.info('Configure Setup 1 (reg: 0x21) - command: 0x{:02x} 0x{:02x} 0x{:02x}'.format(command, byte1, byte2))
		self.spi.mode = SPI_MODE_3
		self.spi.xfer2([command, byte1, byte2])

	def get_data(self, sel):
		#logger.info('Sel: {}'.format(sel[0]['Type']))

		meas_type = sel[0]['Type']
		command = COMMS | RD | DATA 
		logger.info('Get data (0x04) - command: 0x{:02x}'.format(command))

		self.spi.mode = SPI_MODE_3
		rv = self.spi.xfer3([command, PADDING_BYTE, PADDING_BYTE, PADDING_BYTE, PADDING_BYTE])  # 24 bits +  DATA_STAT
		logger.info('Data: 0x{:02x} 0x{:02x} 0x{:02x} 0x{:02x} 0x{:02x}'.format(rv[0], rv[1], rv[2], rv[3], rv[4]))

		sum1 = rv[1]*65536 + rv[2]*256 + rv[3]
		sum2 = sum1*MAX_IN_VOLT/16777215  # 24-bit full scale, 2^24 => 16777216

		if meas_type == '1': # MEAS_VOLT
			logger.info('*** N.B! The result can be scaled via voltage divider. See schematic CDIAG-200:01 00169 ***')
			logger.info('Single Out: {:.1f} V for Channel: {}'.format(sum2, rv[4]&0x0f))  # mask out channel number from byte 4
			return sum2

		if meas_type == '2': # MEAS_DIFF
			logger.info('Diff Out: {:.1f} V for Channel: {}'.format(sum2, rv[4]))
			return sum2

		elif meas_type == '0': # MEAS_CURR
			k = MAX_CURRENT / 16777215.0
			res = sum1*k
			logger.info('Out: {:.1f} mA for Channel: {}'.format(res, rv[4]))
			return res

		else:
			logger.warn('Invalid selection of measuring type: {}'.format(meas_type))
			return 0

	def get_status(self, param):
		command = 0x00 | RD | STATUS
		logger.info('Get Status - command: 0x{:02x}'.format(command))
		self.spi.mode = SPI_MODE_3
		rv = self.spi.xfer2([command, PADDING_BYTE])
		logger.info('0x{:02x}, 0x{:02x}'.format(rv[0], rv[1]))

	def get_offset_gain(self):
		command = 0x00 | RD | OFFSET0
		logger.info('Get Offset 0 - command: 0x{:02x}'.format(command))
		self.spi.mode = SPI_MODE_3
		rv = self.spi.xfer2([command, PADDING_BYTE, PADDING_BYTE, PADDING_BYTE])
		logger.info('0x{:02x} 0x{:02x} 0x{:02x}'.format(rv[1], rv[2], rv[3]))

		command = 0x00 | RD | GAIN0
		logger.info('Get Gain 0 - command: 0x{:02x}'.format(command))
		self.spi.mode = SPI_MODE_3
		rv = self.spi.xfer2([command, PADDING_BYTE, PADDING_BYTE, PADDING_BYTE])
		logger.info('0x{:02x} 0x{:02x} 0x{:02x}\n'.format(rv[1], rv[2], rv[3]))

		command = 0x00 | RD | OFFSET1
		logger.info('Get Offset 1 - command: 0x{:02x}'.format(command))
		self.spi.mode = SPI_MODE_3
		rv = self.spi.xfer2([command, PADDING_BYTE, PADDING_BYTE, PADDING_BYTE])
		logger.info('0x{:02x} 0x{:02x} 0x{:02x}'.format(rv[1], rv[2], rv[3]))

		command = 0x00 | RD | GAIN1
		logger.info('Get Gain 1 - command: 0x{:02x}'.format(command))
		rv = self.spi.xfer2([command, PADDING_BYTE, PADDING_BYTE, PADDING_BYTE])
		self.spi.mode = SPI_MODE_3
		logger.info('0x{:02x} 0x{:02x} 0x{:02x}'.format(rv[1], rv[2], rv[3]))

	def internal_zero_scale(self):
		# internal offset calibration, mode = 100
		command = 0x00 | ADCMODE 
		byte1 = 0x20
		byte2 = 0x40

		logger.info('Calib, internal zero-scale (offset) - command: 0x{:02x} 0x{:02x} 0x{:02x}'.format(command, byte1, byte2))
		self.spi.mode = SPI_MODE_3
		self.spi.xfer2([command, byte1, byte2])

	def internal_full_scale(self):
		# internal gain calibration, mode = 101
		command = 0x00 | ADCMODE 
		byte1 = 0x20
		byte2 = 0x50

		logger.info('Calib, internal full-scale (gain) - command: 0x{:02x} 0x{:02x} 0x{:02x}'.format(command, byte1, byte2))
		self.spi.mode = SPI_MODE_3
		self.spi.xfer2([command, byte1, byte2])

	def system_zero_scale(self):
		# system offset calibration, mode 110
		command = 0x00 | ADCMODE 
		byte1 = 0x20
		byte2 = 0x60

		logger.info('Calib, system zero-scale calib (offset) - command: 0x{:02x} 0x{:02x} 0x{:02x}'.format(command, byte1, byte2))
		self.spi.mode = SPI_MODE_3
		self.spi.xfer2([command, byte1, byte2])

	def system_full_scale(self):
		# system gain calibration, mode 111
		command = 0x00 | ADCMODE 
		byte1 = 0x20
		byte2 = 0x70

		logger.info('Calib, system full-scale calib (gain) - command: 0x{:02x} 0x{:02x} 0x{:02x}'.format(command, byte1, byte2))
		self.spi.mode = SPI_MODE_3
		self.spi.xfer2([command, byte1, byte2])


# --------------------------------------------------------------------------------
# Test purpose functions
# --------------------------------------------------------------------------------
def turn_on_off_5Ve_and_24V(mode):
	if mode == 1:
		print(bcolors.BRED+'Configure Port A and turn ON 5Ve and 24V'+bcolors.ENDC)
		port_write_cmd = 'i2cset -y 1 0x20 0x00 0xc0' # IODIRA
		os.system(port_write_cmd)
		time.sleep(0.1)
		port_write_cmd = 'i2cset -y 1 0x20 0x12 0x18' # GPIOA, 5Ve (R5)
		os.system(port_write_cmd)
		time.sleep(1)
	else:
		print(bcolors.BRED+'Turn OFF 5Ve and 24V'+bcolors.ENDC)
		port_write_cmd = 'i2cset -y 1 0x20 0x12 0x00' # GPIOA
		os.system(port_write_cmd)
		time.sleep(0.1)

def enable_spi0_CE0_1(enable):
	if enable == 1:
		print(bcolors.BYEL+'AD4112 (U406)- Enable CE1, CBA=001 and disable ext reset (RESET from U304)'+bcolors.ENDC)
		port_write_cmd = 'i2cset -y 1 0x20 0x01 0x21' # IODIRB
		os.system(port_write_cmd)
		port_write_cmd = 'i2cset -y 1 0x20 0x13 0x42' # GPIOB
		os.system(port_write_cmd)
		time.sleep(0.1)
	else:
		print('Disable CE2')
		port_write_cmd = 'i2cset -y 1 0x20 0x13 0x00'
		os.system(port_write_cmd)
		time.sleep(0.1)

def enable_spi0_CE0_2(enable):
	if enable == 1:
		print(bcolors.BYEL+'AD4112 (U406)- Enable CE2, CBA=010 and disable ext reset (RESET from U304)'+bcolors.ENDC)
		port_write_cmd = 'i2cset -y 1 0x20 0x01 0x21' # IODIRB
		os.system(port_write_cmd)
		port_write_cmd = 'i2cset -y 1 0x20 0x13 0x44' # GPIOB
		os.system(port_write_cmd)
		time.sleep(0.1)
	else:
		print('Disable CE2')
		port_write_cmd = 'i2cset -y 1 0x20 0x13 0x00'
		os.system(port_write_cmd)
		time.sleep(0.1)

def get_identity_device_0(obj):
	_ID = '0x07'
	_CH0 = '0x10'

	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_ID}
	obj.configure(item)

def get_identity_device_1(obj):
	_ID = '0x07'
	_CH0 = '0x10'

	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_ID}
	obj.configure(item)

def gpo_test(obj):
	_GPIOCON = '0x06'
	_GP_DATA0 = '0x40'  # bit 6 in GPIOCON, U406:25
	_GP_DATA1 = '0x80'  # bit 7 in GPIOCON, U406:38
	_ON = '1'
	_OFF = '0'

	item1 = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_GPIOCON, 'GP':_GP_DATA0, 'Mode':_ON}
	item2 = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_GPIOCON, 'GP':_GP_DATA0, 'Mode':_OFF}

	obj.configure(item1)
	time.sleep(2)
	obj.configure(item2)
	time.sleep(2)

	item3 = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_GPIOCON, 'GP':_GP_DATA1, 'Mode':_ON}
	item4 = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_GPIOCON, 'GP':_GP_DATA1, 'Mode':_OFF}

	obj.configure(item3)
	time.sleep(2)
	obj.configure(item4)
	time.sleep(2)

	print(DELIMITER*'-')

def setup_and_measure_ch6_simple_way(obj):
	# This is done with direct access to the functions
	vec = CH_EN | SETUP_SEL_0 | INPUT_VIN6
	obj.config_channel_reg(CH6, vec)
	time.sleep(DELAY_01s)

	vec = REF_BUFP | REF_BUFM | INBUF_EN
	obj.config_setup(vec)
	time.sleep(DELAY_01s)

	vec = REF_EN | SING_SYNC | SING_CONV
	obj.config_adc_mode(vec)
	time.sleep(DELAY_01s)

	vec = DATA_STAT
	obj.config_interface_mode(vec)
	time.sleep(DELAY_01s)

	obj.get_data(MEAS_VOLT)
	time.sleep(DELAY_02s)

def setup_and_measure_device_0_ch0(obj):
	print(bcolors.BYEL+'Device 0, Channel 0'+bcolors.ENDC)

	_CH0 = '0x10'
	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_CH0}
	obj.configure(item)
	time.sleep(DELAY_01s)

	_SETUPCON0 = '0x20'
	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_SETUPCON0}
	obj.configure(item)
	time.sleep(DELAY_01s)

	_ADCMODE = '0x01'
	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_ADCMODE}
	obj.configure(item)

	_IFMODE = '0x02'
	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_IFMODE}
	obj.configure(item)

	_DATA = '0x04'
	_MEAS_VOLT = '1'
	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_DATA, 'Type':_MEAS_VOLT}
	rv = obj.configure(item)

	_STATUS = '0x00'
	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_STATUS}
	obj.configure(item)

	rv_round = round(rv, 1)
	print(bcolors.BYEL+'Voltage at CH0: {0:.1f}V'.format(rv_round)+bcolors.ENDC)
	return rv_round

def setup_and_measure_device_0_ch4(obj):
	print(bcolors.BYEL+'Device 0, Channel 4'+bcolors.ENDC)

	_CH4 = '0x14'
	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_CH4}
	obj.configure(item)
	time.sleep(DELAY_01s)

	_SETUPCON0 = '0x20'
	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_SETUPCON0}
	obj.configure(item)
	time.sleep(DELAY_01s)

	_ADCMODE = '0x01'
	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_ADCMODE}
	obj.configure(item)

	_IFMODE = '0x02'
	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_IFMODE}
	obj.configure(item)

	_DATA = '0x04'
	_MEAS_VOLT = '1'
	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_DATA, 'Type':_MEAS_VOLT}
	rv = obj.configure(item)

	_STATUS = '0x00'
	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_STATUS}
	obj.configure(item)

	rv_round = round(rv, 1)
	print(bcolors.BYEL+'Voltage at CH4: {0:.1f}V'.format(rv_round)+bcolors.ENDC)
	return rv_round

def setup_and_measure_device_0_ch6(obj):
	print(bcolors.BYEL+'Device 0, Channel 6'+bcolors.ENDC)

	_CH6 = '0x16'
	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_CH6}
	obj.configure(item)
	time.sleep(DELAY_01s)

	_SETUPCON0 = '0x20'
	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_SETUPCON0}
	obj.configure(item)
	time.sleep(DELAY_01s)

	_ADCMODE = '0x01'
	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_ADCMODE}
	obj.configure(item)

	_IFMODE = '0x02'
	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_IFMODE}
	obj.configure(item)

	_DATA = '0x04'
	_MEAS_VOLT = '1'
	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_DATA, 'Type':_MEAS_VOLT}
	rv = obj.configure(item)

	_STATUS = '0x00'
	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_STATUS}
	obj.configure(item)

	rv_round = round(rv, 1)
	print(bcolors.BYEL+'Voltage at CH6: {0:.1f}V'.format(rv_round)+bcolors.ENDC)
	return rv_round

def setup_and_measure_device_1_ch0(obj):
	_CH0 = '0x10'
	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_CH0}
	obj.configure(item)
	time.sleep(DELAY_01s)

	_SETUPCON0 = '0x20'
	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_SETUPCON0}
	obj.configure(item)
	time.sleep(DELAY_01s)

	_ADCMODE = '0x01'
	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_ADCMODE}
	obj.configure(item)

	_IFMODE = '0x02'
	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_IFMODE}
	obj.configure(item)

	_DATA = '0x04'
	_MEAS_VOLT = '1'
	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_DATA, 'Type':_MEAS_VOLT}
	rv = obj.configure(item)

	_STATUS = '0x00'
	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_STATUS}
	obj.configure(item)

	rv_round = round(rv, 1)
	print(bcolors.BYEL+'Voltage at CH0: {0:.1f}V'.format(rv_round)+bcolors.ENDC)
	return rv_round

def setup_and_measure_device_1_ch6(obj):
	print(bcolors.BYEL+'Device 1, Channel 6'+bcolors.ENDC)

	_CH6 = '0x16'
	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_CH6}
	obj.configure(item)
	time.sleep(DELAY_01s)

	_SETUPCON0 = '0x20'
	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_SETUPCON0}
	obj.configure(item)
	time.sleep(DELAY_01s)

	_ADCMODE = '0x01'
	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_ADCMODE}
	obj.configure(item)

	_IFMODE = '0x02'
	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_IFMODE}
	obj.configure(item)

	_DATA = '0x04'
	_MEAS_VOLT = '1'
	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_DATA, 'Type':_MEAS_VOLT}
	rv = obj.configure(item)

	_STATUS = '0x00'
	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_STATUS}
	obj.configure(item)

	rv_round = round(rv, 1)
	print(bcolors.BYEL+'Voltage at CH6: {0:.1f}V'.format(rv_round)+bcolors.ENDC)
	return rv_round

def setup_and_measure_device_1_ch7(obj):
	_CH7 = '0x17'
	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_CH7}
	obj.configure(item)
	time.sleep(DELAY_01s)

	_SETUPCON0 = '0x20'
	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_SETUPCON0}
	obj.configure(item)
	time.sleep(DELAY_01s)

	_ADCMODE = '0x01'
	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_ADCMODE}
	obj.configure(item)

	_IFMODE = '0x02'
	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_IFMODE}
	obj.configure(item)

	_DATA = '0x04'
	_MEAS_VOLT = '1'
	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_DATA, 'Type':_MEAS_VOLT}
	rv = obj.configure(item)

	_STATUS = '0x00'
	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_STATUS}
	obj.configure(item)

	rv_round = round(rv, 1)
	print(bcolors.BYEL+'Voltage at CH7: {0:.1f}V'.format(rv_round)+bcolors.ENDC)
	return rv_round

def calibrate(obj, calib_mode):
	if calib_mode == INT_OFFSET:
		obj.internal_zero_scale()
	elif calib_mode == INT_GAIN:
		obj.internal_full_scale()
	elif calib_mode == SYSTEM_OFFSET:
		obj.system_zero_scale()
	elif calib_mode == SYSTEM_GAIN:
		obj.system_full_scale()
	else:
		print('Invalid calibration mode')

	time.sleep(0.6)

def main():
	#turn_on_off_5Ve_and_24V(ON)
	myAD = ad4112()

	if len(sys.argv) > 1:
		if sys.argv[1] == 'reset':
			myAD.device_reset()
			time.sleep(DELAY_1s)
		elif sys.argv[1] == 'io':
			calibrate(myAD, INT_OFFSET)
		elif sys.argv[1] == 'ig':
			calibrate(myAD, INT_GAIN)
		elif sys.argv[1] == 'so':
			calibrate(myAD, SYSTEM_OFFSET)
		elif sys.argv[1] == 'sg':
			calibrate(myAD, SYSTEM_GAIN)
		else:
			print('Nope')


	#myAD.update_gain(GAIN0, [0xd5, 0x97, 0xda])
	#myAD.update_gain(GAIN1, [0xd5, 0x97, 0xda])

	# =========================================================
	# Below a number of test cases have been implemented.
	# To use them, comment/uncomment to select the test case
	# you want to run.
	# =========================================================


	# ---------------------------------------------------
	# Test of GPO0 and GPO1, U406:25, 38
	#gpo_test(myAD)
	#time.sleep(DELAY_01s)
	# ---------------------------------------------------

	enable_spi0_CE0_1(1)
	# ---------------------------------------------------
	# Test of ch0 on U405:2 (VIN0), device 0, J2:7
	get_identity_device_0(myAD)
	time.sleep(DELAY_01s)

	#setup_and_measure_device_0_ch0(myAD)
	setup_and_measure_device_0_ch4(myAD)
	time.sleep(DELAY_2s)
	# ---------------------------------------------------

	#enable_spi0_CE0_2(1)
	# ---------------------------------------------------
	# Test of ch0 on U406:2 (VIN0), device 0, J2:19
	#get_identity_device_1(myAD)
	#time.sleep(DELAY_01s)

	#setup_and_measure_device_1_ch0(myAD)
	#time.sleep(DELAY_2s)
	# ---------------------------------------------------

	# ---------------------------------------------------
	# Test of ch6 on U406:28 (VIN6), device 0, J2:17
	#get_identity_device_1(myAD)
	#time.sleep(DELAY_01s)

	#setup_and_measure_device_1_ch6(myAD)
	#time.sleep(DELAY_2s)
	# ---------------------------------------------------

	# ---------------------------------------------------
	# Test of ch7 on U406:29 (VIN7), device 0, J2:18
	#get_identity_device_1(myAD)
	#time.sleep(DELAY_01s)

	#setup_and_measure_device_1_ch7(myAD)
	#time.sleep(DELAY_2s)
	# ---------------------------------------------------


	# ---------------------------------------------------
	# Test of differential input.
	# Connect +V to VIN0 and GND to VIN1.
	# Did'nt need to send reset.
	#setup = CH_EN | SETUP_SEL_0 | INPUT_VIN6_VIN7
	#myAD.config_channel_reg(CH6, setup)
	#setup = CH_EN | SETUP_SEL_0 | INPUT_VIN6_VIN7
	#myAD.config_channel_reg(CH7, setup)

	#vec = BI_POLAR | REF_BUFP | REF_BUFM | INBUF_EN 
	#myAD.config_setup(vec)

	#setup = REF_EN | SING_SYNC | SING_CONV
	#myAD.config_adc_mode(setup)

	#setup = DATA_STAT
	#myAD.config_interface_mode(setup)

	#myAD.get_data(MEAS_DIFF)
	#time.sleep(DELAY_01s)
	# ---------------------------------------------------


	# ---------------------------------------------------
	# Test of Current inputs.
	# Connect to II0+ and GND.
	#setup = CH_EN | SETUP_SEL_0 | IIN0
	#myAD.config_channel_reg(CH0, setup)

	#setup = REF_BUFP | REF_BUFM | INBUF_EN
	#myAD.config_setup(setup)

	#setup = REF_EN | SING_SYNC | SING_CONV
	#myAD.config_adc_mode(setup)

	#setup = DATA_STAT
	#myAD.config_interface_mode(setup)

	#myAD.get_data(MEAS_CURR)
	#time.sleep(DELAY_01s)
	# ---------------------------------------------------


	#myAD.get_offset_gain()
	#time.sleep(DELAY_01s)

	#myAD.get_status()
	#turn_on_off_5Ve_and_24V(OFF)


if __name__ == '__main__':
	main()
