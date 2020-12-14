import os
import sys
import time

# Safety MCP23017 (addr=1)
S1 = 0
S2 = 1
READY = 2
SAFE =  3
RESET = 4


# Relay index controlled by MCP23017 (addr=0)
DC_300V = 0
AC_230V = 1
PROTECTED_EARTH = 2
p_24V = 3
p_5eV = 4
END_PWR = 5

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
END_RELAY = 16

# Misc defines
ON = 1
OFF = 0

# MCP23017
MCP23017_DEVICE_0 = 0x20
MCP23017_DEVICE_1 = 0x21
I2C_GPIOA = 0x14
I2C_GPIOB = 0x15


class bcolors:
	RED = '\033[91m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	BOLD = '\033[1m'
	ENDC = '\033[0m'


def send_command(cmd):
	os.system(cmd)


class mcp_io_ctrl():
	def __init__(self):
		# Port GPA0 - GPA5 output
		#port_write_cmd = 'i2cset -y 1 0x20 0x00 0x3f'
		#send_command(port_write_cmd)
		self.power_bit_vector = 0x00
		self.relay_bit_vector = 0x00

	def power_ctrl(self, sel_power, mode):
		if sel_power < END_PWR:

			if mode == ON:
				self.power_bit_vector |= (1 << sel_power)

			elif mode == OFF:
				self.power_bit_vector &= ~(1 << sel_power)
			else:
				print('Err: Invalid selection of mode')
				return 0

			port_write_cmd = 'i2cset -y 1' +\
					 ' 0x%02x' % MCP23017_DEVICE_0 +\
					 ' 0x%02x' % I2C_GPIOA +\
					 ' 0x%02x' % self.power_bit_vector

			print('Power: {}, Mode: {}, cmd: {}'.format(self._mcp23017_get_power_name(sel_power), 
			                                            self._mcp23017_get_mode_name(mode), 
								    port_write_cmd))
			#os.system(port_write_cmd)
			return 1

		else:
			print('Err: Invalid selection of power')
			return 0

	def relay_ctrl(self, relay, mode):
		if relay < END_RELAY:

			if mode == ON:
				self.relay_bit_vector |= (1 << relay)
			elif mode == OFF:
				self.relay_bit_vector &= ~(1 << relay)
			else:
				print('Err: Invalid selection of mode')
				return 0

			port_write_cmd = 'i2cset -y 1' +\
					 ' 0x%02x' % MCP23017_DEVICE_1 +\
					 ' 0x%02x' % I2C_GPIOA +\
					 ' 0x%02x' % self.relay_bit_vector

			print('Relay: {}, Mode: {}, cmd: {}'.format(self._mcp23017_get_relay_name(relay), 
			                                            self._mcp23017_get_mode_name(mode), 
								    port_write_cmd))
			#os.system(port_write_cmd)
			return 1

		else:
			print('Err: Invalid selection of relay')
			return 0

	def _mcp23017_get_power_name(self, inp):
		if inp == DC_300V:
			return 'DC_300V'
		elif inp == AC_230V:
			return 'AC_230V'
		elif inp == PROTECTED_EARTH:
			return 'PROTECTED_EARTH'
		elif inp == p_24V:
			return 'p_24V'
		elif inp == p_5eV:
			return 'p_5eV'
		else:
			return 'Invalid input'

	def _mcp23017_get_relay_name(self, inp):
		if inp == RELAY1:
			return 'RELAY1'
		if inp == RELAY2:
			return 'RELAY2'
		if inp == RELAY3:
			return 'RELAY3'
		else:
			return 'Invalid input'

	def _mcp23017_get_mode_name(self, inp):
		if inp == ON:
			return 'ON'
		if inp == OFF:
			return 'OFF'
		else:
			return 'Invalid input'

	def teardown(self):
		print('Teardown')
		# Set Port GPA0 - GPA5 input
		#port_write_cmd = 'i2cset -y 1 0x20 0x00 0x00'
		#send_command(port_write_cmd)
		self.power_bit_vector = 0x00


def main():
	io_ctrl = mcp_io_ctrl()

	rv = io_ctrl.power_ctrl(DC_300V, ON)
	#rv = io_ctrl.power_ctrl(AC_230V, ON)
	#rv = io_ctrl.power_ctrl(PROTECTED_EARTH, ON)
	#rv = io_ctrl.power_ctrl(p_24V, ON)
	#rv = io_ctrl.power_ctrl(p_5eV, ON)
	#rv = io_ctrl.power_ctrl(p_5eV, 3)

	print(60*'-')

	#rv = io_ctrl.power_ctrl(DC_300V, OFF)
	#rv = io_ctrl.power_ctrl(AC_230V, OFF)
	#rv = io_ctrl.power_ctrl(PROTECTED_EARTH, OFF)
	#rv = io_ctrl.power_ctrl(p_24V, OFF)
	#rv = io_ctrl.power_ctrl(p_5eV, OFF)

	#print(60*'-')

	io_ctrl.relay_ctrl(RELAY1, ON)
	#io_ctrl.relay_ctrl(RELAY2, ON)
	#io_ctrl.relay_ctrl(RELAY3, ON)

	#print(60*'-')

	#io_ctrl.relay_ctrl(RELAY1, OFF)
	#io_ctrl.relay_ctrl(RELAY2, OFF)
	#io_ctrl.relay_ctrl(RELAY3, OFF)

	#io_ctrl.teardown()


if __name__ == '__main__':
	main()

