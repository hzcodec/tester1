#
# The script is turning ON or OFF 5Ve and 24V
#
# To turn on/off 5Ve/24V:
#     python3 turn_on_powers.py
#
#     Make a selection accordingly.

import os
import sys
import time

class bcolors:
	RED = '\033[91m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	BOLD = '\033[1m'
	ENDC = '\033[0m'


def send_command(cmd):
	os.system(cmd)


# Addr 0, Port A5-0 output
port_write_cmd = 'i2cset -y 1 0x20 0x00 0xc0'
send_command(port_write_cmd)


def main():

	key = 'dummy'

	while (key != 'q'):
		key = input('1=5Ve and 24V ON, 2=5Ve and 24V OFF, q=exit -> ')

		if (key == '1'):
			print(bcolors.GREEN+'5Ve and 24V ON'+bcolors.ENDC)
		
			port_write_cmd = 'i2cset -y 1 0x20 0x12 0x18'
			os.system(port_write_cmd)

		elif (key == '2'):
			print(bcolors.RED+'5Ve and 24V OFF'+bcolors.ENDC)
		
			port_write_cmd = 'i2cset -y 1 0x20 0x12 0x00'
			os.system(port_write_cmd)
		

if __name__ == '__main__':
	main()

