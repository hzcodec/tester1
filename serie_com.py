from robot.api import logger
import sys

sys.path.insert(0, './220_04_062')
from common_files.common import *
import ast
import serial
import logging
import time
import glob
import sys

logging.basicConfig(level=logging.DEBUG)


class serie_com():
	ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

	def __init__(self):
		self.serial_port_is_available = False
		self.result = []
		self.ai1 = ''
		self.ai2 = ''
		self.ai3 = ''
		self.ai4 = ''

	def _find_serial_ports(self):
		ports = glob.glob('/dev/ttyACM*')
		logger.info('Ports: {}'.format(ports))

		if ports:
			self.result.append(ports[0])

		return self.result

	def setup_serial_port(self):
		available_serial_ports = self._find_serial_ports()
		logger.info('Available ports: {}'.format(available_serial_ports))
		# During developmet:
		# For serial communication with commands like di and do => /dev/ttyACM0

		if available_serial_ports:
			self.ser = serial.Serial()
			#self.ser.port = available_serial_ports[0]
			self.ser.port = '/dev/ttyACM0'
			self.ser.baudrate = 38400
			self.ser.timeout = 3  # non-block read
			self.ser.parity = serial.PARITY_EVEN
			self.ser.stopbits = serial.STOPBITS_ONE
			self.ser.bytesize = serial.EIGHTBITS
			self.ser.open()

			#Check if serial port has been opened correctly
			if (self.ser.is_open):
				logger.info("Serial port is open")
				self.serial_port_is_available = True
			else:
				logger.warn("Failed to connect Serial Port")

			logger.info('Name: {}, Port: {}'.format(self.ser.name, self.ser.port))
		else:
			self.serial_port_is_available = False
			logger.warn('No port is available for serial communication')

	def serial_write_cmd(self, cmd):
		if self.serial_port_is_available:
			command_to_send = (cmd+"\r")
	
			for c in command_to_send:
					self.ser.reset_output_buffer()
					self.ser.write(c.encode("utf-8"))
					time.sleep(0.1)

	def serial_write_cmd2(self, cmd):
		if self.serial_port_is_available:
			command_to_send = (cmd+"\r")
	
			for c in command_to_send:
					self.ser.reset_output_buffer()
					self.ser.write(c.encode("utf-8"))
					time.sleep(0.1)
					logger.info('Command {}'.format(cmd))

		time.sleep(0.5)
		read_string = ""

		while self.ser.inWaiting() > 0:
			#read_string += self.ser.readline().decode('utf-8', errors='replace')
			read_string = self.ser.readline().decode('utf-8', errors='replace')
			logger.info('inWaiting: {}'.format(read_string))

			if read_string[0:3] == 'AI1':
				self.ai1 = read_string[0:]
			if read_string[0:3] == 'AI2':
				self.ai2 = read_string[0:]
			if read_string[0:3] == 'AI3':
				self.ai3 = read_string[0:]
			if read_string[0:3] == 'AI4':
				self.ai4 = read_string[0:]

		return read_string

	def serial_cmd(self, cmd):
		command_to_send = (cmd+"\r")
		self.ser.reset_output_buffer()

		for c in command_to_send:
			self.ser.write(c.encode("utf-8"))
			time.sleep(0.1)
			logger.info('cmd di')

		time.sleep(0.5)
		read_string = ""

		while self.ser.inWaiting() > 0:
			read_string += self.ser.readline().decode('utf-8', errors='replace')
			logger.info('inWaiting')

		#logger.info('Read string: {}'.format(read_string))
		return read_string

	#[TODO]: This need to be refactored/changed
	def receive_data_communication_port(self):
		logger.info('Receive data from Communication Port')

		cmd = 'rx_comm'
		rv = serial_cmd(cmd)
		
		rv_json = json.loads(rv[7:]) # get rid of first chararcters ('rx_comm')
		logger.info('Rec: {}'.format(rv_json['rx_communication_channel']))
		
		if rv_json['rx_communication_channel'] == 'Banankontakt':
			return 1
		else:
			return 0

	def get_version(self):
		logger.info('Get software version number')
		self.serial_write_cmd('\rversion\r')
		time.sleep(4)
		self.serial_write_cmd('\rversion\r')
		time.sleep(4)

	def red_led_test(self):
		cmd = '\rdo DOUT_LED_RED 0'  # \r to get rid of garbage
		self.serial_write_cmd(cmd)
		logger.info('Red LED OFF')

		cmd = 'do DOUT_LED_RED 1'
		self.serial_write_cmd(cmd)
		logger.info('Red LED ON')

	def green_led_test(self):
		cmd = '\rdo DOUT_LED_GREEN 0'
		self.serial_write_cmd(cmd)
		logger.info('Green LED OFF')

		cmd = 'do DOUT_LED_GREEN 1'
		self.serial_write_cmd(cmd)
		logger.info('Green LED ON')

	def yellow_led_test(self):
		cmd = '\rdo DOUT_LED_YELLOW 0'
		self.serial_write_cmd(cmd)
		logger.info('Yellow LED OFF')

		cmd = 'do DOUT_LED_YELLOW 1'
		self.serial_write_cmd(cmd)
		logger.info('Yellow LED ON')

	def he_ok_all_led_test(self):
		logger.info('HE_OK all LED ON')
		cmd = '\rdo DOUT_HE_1_OK 1'
		self.serial_write_cmd(cmd)

		cmd = '\rdo DOUT_HE_2_OK 1'
		self.serial_write_cmd(cmd)

		cmd = '\rdo DOUT_HE_3_OK 1'
		self.serial_write_cmd(cmd)

		cmd = '\rdo DOUT_HE_4_OK 1'
		self.serial_write_cmd(cmd)

		cmd = '\rdo DOUT_HE_5_OK 1'
		self.serial_write_cmd(cmd)

		cmd = '\rdo DOUT_HE_6_OK 1'
		self.serial_write_cmd(cmd)

		logger.info('HE_OK all LED OFF')
		cmd = '\rdo DOUT_HE_1_OK 0'
		self.serial_write_cmd(cmd)

		cmd = '\rdo DOUT_HE_2_OK 0'
		self.serial_write_cmd(cmd)

		cmd = '\rdo DOUT_HE_3_OK 0'
		self.serial_write_cmd(cmd)

		cmd = '\rdo DOUT_HE_4_OK 0'
		self.serial_write_cmd(cmd)

		cmd = '\rdo DOUT_HE_5_OK 0'
		self.serial_write_cmd(cmd)

		cmd = '\rdo DOUT_HE_6_OK 0'
		self.serial_write_cmd(cmd)

	def he_err_all_led_test(self):
		logger.info('HE_ERR all LED ON')
		cmd = '\rdo DOUT_HE_1_ERR 1'
		self.serial_write_cmd(cmd)

		cmd = '\rdo DOUT_HE_2_ERR 1'
		self.serial_write_cmd(cmd)

		cmd = '\rdo DOUT_HE_3_ERR 1'
		self.serial_write_cmd(cmd)

		cmd = '\rdo DOUT_HE_4_ERR 1'
		self.serial_write_cmd(cmd)

		cmd = '\rdo DOUT_HE_5_ERR 1'
		self.serial_write_cmd(cmd)

		cmd = '\rdo DOUT_HE_6_ERR 1'
		self.serial_write_cmd(cmd)

		logger.info('HE_ERR all LED OFF')
		cmd = '\rdo DOUT_HE_1_ERR 0'
		self.serial_write_cmd(cmd)

		cmd = '\rdo DOUT_HE_2_ERR 0'
		self.serial_write_cmd(cmd)

		cmd = '\rdo DOUT_HE_3_ERR 0'
		self.serial_write_cmd(cmd)

		cmd = '\rdo DOUT_HE_4_ERR 0'
		self.serial_write_cmd(cmd)

		cmd = '\rdo DOUT_HE_5_ERR 0'
		self.serial_write_cmd(cmd)

		cmd = '\rdo DOUT_HE_6_ERR 0'
		self.serial_write_cmd(cmd)

	def he_ok_led_test(self, led, mode):
		led_int = int(led)
		mode_int = int(mode)

		cmd = '\rdo DOUT_HE_{}_OK {}'.format(n_int, mode_int)
		self.serial_write_cmd(cmd)

	def he_err_led_test(self, led, mode):
		led_int = int(led)
		mode_int = int(mode)

		cmd = '\rdo DOUT_HE_{}_ERR {} {}'.format(led_int, mode_int)
		self.serial_write_cmd(cmd)

	def led1_and_led2_test(self):
		cmd = '\rdo DOUT_LED_LED1 1'  # \r to get rid of garbage
		self.serial_write_cmd(cmd)
		logger.info('LED1 (green) ON')

		cmd = 'do DOUT_LED_LED2 1'
		self.serial_write_cmd(cmd)
		logger.info('LED2 (blue) ON')

		cmd = 'do DOUT_LED_LED1 0'
		self.serial_write_cmd(cmd)
		logger.info('LED1 (green) OFF')

		cmd = 'do DOUT_LED_LED2 0'
		self.serial_write_cmd(cmd)
		logger.info('LED2 (blue) OFF')

	def can_led_test(self):
		cmd = '\rdo DOUT_CAN_OK 1'
		self.serial_write_cmd(cmd)
		logger.info('CAN_OK LED ON')

		cmd = 'do DOUT_CAN_OK 0'
		self.serial_write_cmd(cmd)
		logger.info('CAN_OK LED OFF')

		cmd = 'do DOUT_CAN_ERR 1'
		self.serial_write_cmd(cmd)
		logger.info('CAN_ERR LED ON')

		cmd = 'do DOUT_CAN_ERR 0'
		self.serial_write_cmd(cmd)
		logger.info('CAN_ERR LED OFF')

	def drive_led_test(self):
		cmd = '\rdo DOUT_DRV_OK 1'
		self.serial_write_cmd(cmd)
		logger.info('DRV_OK LED ON')

		cmd = 'do DOUT_DRV_OK 0'
		self.serial_write_cmd(cmd)
		logger.info('CAN_DRV LED OFF')

		cmd = 'do DOUT_DRV_ERR 1'
		self.serial_write_cmd(cmd)
		logger.info('DRV_ERR LED ON')

		cmd = 'do DOUT_DRV_ERR 0'
		self.serial_write_cmd(cmd)
		logger.info('DRV_ERR LED OFF')

	def digital_do_test(self, port, level):
		cmd = '\rdo DOUT_PLC_DO_{} {}'.format(port, level)
		self.serial_write_cmd(cmd)
		logger.info('cmd: {}'.format(cmd))

	def digital_doc_test(self, port, level):
		cmd = '\rdo DOUT_PLC_DOC_{} {}'.format(port, level)
		self.serial_write_cmd(cmd)
		logger.info('cmd: {}'.format(cmd))

	def low_current_test_1(self):
		logger.info('Set port 1-3-5 high')
		cmd = '\rdo DOUT_PLC_DO_1 1'
		self.serial_write_cmd(cmd)
		cmd = 'do DOUT_PLC_DO_3 1'
		self.serial_write_cmd(cmd)
		cmd = 'do DOUT_PLC_DO_5 1'
		self.serial_write_cmd(cmd)

	def low_current_test_2(self):
		logger.info('Set port 2-4 high')
		cmd = '\rdo DOUT_PLC_DO_1 0'
		self.serial_write_cmd(cmd)
		cmd = 'do DOUT_PLC_DO_3 0'
		self.serial_write_cmd(cmd)
		cmd = 'do DOUT_PLC_DO_5 0'
		self.serial_write_cmd(cmd)

		cmd = 'do DOUT_PLC_DO_2 1'
		self.serial_write_cmd(cmd)
		cmd = 'do DOUT_PLC_DO_4 1'
		self.serial_write_cmd(cmd)

	def high_current_test_1(self):
		logger.info('Set port 1-3-5-7 high')
		cmd = '\rdo DOUT_PLC_DOC_1 1'
		self.serial_write_cmd(cmd)
		cmd = 'do DOUT_PLC_DOC_3 1'
		self.serial_write_cmd(cmd)
		cmd = 'do DOUT_PLC_DOC_5 1'
		self.serial_write_cmd(cmd)
		cmd = 'do DOUT_PLC_DOC_7 1'
		self.serial_write_cmd(cmd)

	def high_current_test_2(self):
		logger.info('Set port 2-4-6 high')
		cmd = '\rdo DOUT_PLC_DOC_1 0'
		self.serial_write_cmd(cmd)
		cmd = 'do DOUT_PLC_DOC_3 0'
		self.serial_write_cmd(cmd)
		cmd = 'do DOUT_PLC_DOC_5 0'
		self.serial_write_cmd(cmd)
		cmd = 'do DOUT_PLC_DOC_7 0'
		self.serial_write_cmd(cmd)

		cmd = 'do DOUT_PLC_DOC_2 1'
		self.serial_write_cmd(cmd)
		cmd = 'do DOUT_PLC_DOC_4 1'
		self.serial_write_cmd(cmd)
		cmd = 'do DOUT_PLC_DOC_6 1'
		self.serial_write_cmd(cmd)

	def teardown_serial_port(self):
		if self.serial_port_is_available:
			logger.info('Serial port is closed')
			self.ser.flush()
			self.ser.close()

	def get_di_1_to_7(self, test):
		#rv = self.serial_write_cmd2('di')

		# convert string to dictionary 
		#res = ast.literal_eval(rv)

		## get di from dictionary only
		#di_items = {k: res[k] for k in list(res)[:7]}

		#test_int = int(test)
		#if test == 1:
		#	logger.info('*** Test 1')
		#	if di_items['DI1'] != 1:
		#		return 0
		#	if di_items['DI2'] != 0:
		#		return 0
		#	if di_items['DI3'] != 1:
		#		return 0
		#	if di_items['DI4'] != 0:
		#		return 0
		#	if di_items['DI5'] != 1:
		#		return 0
		#	if di_items['DI6'] != 0:
		#		return 0
		#	if di_items['DI7'] != 1:
		#		return 0
		#elif test == 2:
		#	logger.info('*** Test 2')
		#	if di_items['DI1'] != 0:
		#		return 0
		#	if di_items['DI2'] != 1:
		#		return 0
		#	if di_items['DI3'] != 0:
		#		return 0
		#	if di_items['DI4'] != 1:
		#		return 0
		#	if di_items['DI5'] != 0:
		#		return 0
		#	if di_items['DI6'] != 1:
		#		return 0
		#	if di_items['DI7'] != 0:
		#		return 0

		return 1

	def read_analog_in(self):
		logger.info('Read Analog IN')
		cmd = '\rstatus'

		#self.ser.flushInput()
		#self.ser.flushOutput()
		time.sleep(0.1)

		#rv = self.serial_write_cmd2(cmd)

		rv = self.check_analog_result()
		return rv

	def check_analog_result(self):

		#int_ai1 = int(self.ai1[5:])
		#int_ai2 = int(self.ai2[5:])
		#int_ai3 = int(self.ai3[5:])
		#int_ai4 = int(self.ai4[5:])

		#logger.info('AI1: {}'.format((int_ai1)))
		#logger.info('AI2: {}'.format((int_ai2)))
		#logger.info('AI3: {}'.format((int_ai3)))
		#logger.info('AI4: {}'.format((int_ai4)))

		## The unit for the values are uA.
		#if (int_ai1 > 17800 or int_ai1 < 16500):
		#	return 0
		#if (int_ai2 > 9500 or int_ai2 < 8250):
		#	return 0
		#if (int_ai3 > 13800 or int_ai3 < 12500):
		#	return 0
		#if (int_ai4 > 5400 or int_ai4 < 4600):
		#	return 0
		#else:
			#return 1
		return 1

	def set_identity(self, identity):
		logger.info('Set Identity: {}'.format(identity))

		cmd = '\r v'
		self.serial_write_cmd(cmd)

		cmd = identity
		self.serial_write_cmd(cmd)

		cmd = '\r v'
		self.serial_write_cmd(cmd)

		self.get_version()


# ========================================================================================
# Individual tests called from main()

def led_test_rgy(obj):
	obj.red_led_test()
	obj.green_led_test()
	obj.yellow_led_test()

def led_test_can(obj):
	obj.can_led_test()

def do_test(obj):
	for port in DO_PORTS:
		obj.digital_do_test(port, ON)
		obj.digital_do_test(port, OFF)

def doc_test(obj):
	for port in DOC_PORTS:
		obj.digital_doc_test(port, ON)
		obj.digital_doc_test(port, OFF)

# ========================================================================================


def main():
	# N.B! 24Ve and 5Ve shall be on

	ser_com = serie_com()
	ser_com.setup_serial_port()

	led_test_rgy(ser_com)
	#led_test_can(ser_com)

	#do_test(ser_com)
	#doc_test(ser_com)

	time.sleep(DELAY_05s)
	ser_com.teardown_serial_port()


if __name__ == '__main__':
        main()

