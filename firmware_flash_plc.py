import os
import time
import glob
import json
import logging
import subprocess
import sys
from robot.api import logger
from robot.utils.asserts import assert_equal, assert_true, assert_none, fail

DELAY_1s = 1
DELAY_3s = 3
TIMEOUT = 35

logging.basicConfig(level=logging.DEBUG)

BOOT_LOADER         = "HCF-220_02_137_RA.elf"
TEST_FIRMWARE       = "HCF-220_02_202.hex"

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def flash_bootloader_and_test_application():
	logger.info('Flash PLC with: {} - {}'.format(BOOT_LOADER, TEST_FIRMWARE))

	os.system('openocd -f openocd.cfg -c init -c "epv bin/{} bin/{}; exit"'.format(BOOT_LOADER, TEST_FIRMWARE))
	time.sleep(DELAY_1s)
	return 1

def reset_and_start_application():
	logger.info('Reset and Start PLC')

	os.system('openocd -f openocd.cfg -c init -c "boot_reset; exit"')
	time.sleep(DELAY_1s)
	return 1

# The sheer fact that this function is here is just an anomaly :-)
# If you have a better idea where to put it then - 
# Speak out now or forever hold their peace.
def read_identification_file():
	with open('id_file.txt') as json_file:
		json_data = json.load(json_file)

	logger.info(json_data)

	if json_data["Project Number"] != "500:01 177":
		logger.warn('Incorrect Project number: {}'.format(json_data["Project Number"]))
		return 0

	if json_data["Unicorn Board number"] != "210:01 154 RB":
		logger.warn('Incorrect Board number: {}'.format(json_data["Unicorn Board number"]))
		return 0

	if json_data["Adapter Board number"] != "210:01 155 RA":
		logger.warn('Incorrect Board number: {}'.format(json_data["Adapter Board number"]))
		return 0

	return 1


def headline():
	print("1 = Flash bootloader and Test application")
	print("2 = Reset and start Test application")
	print("q = Quit script")

def send_command(cmd):
	os.system(cmd)


def main():

	# Addr 0, Port A5-0 output
	port_write_cmd = 'i2cset -y 1 0x20 0x00 0xc0'
	send_command(port_write_cmd)

	headline()
	key = input("Select operation - ")

	if key != 'q':

		# Turn on 5Ve and 24V (R4, R5)
		port_write_cmd = 'i2cset -y 1 0x20 0x12 0x18'
		send_command(port_write_cmd)
		time.sleep(DELAY_3s)

		while key != 'q':

			if (key == '1'):
				print(bcolors.GREEN+20*'-'+'*** Flash Bootloader/Test application ***'+20*'-'+bcolors.ENDC)
				flash_bootloader_and_test_application()

			if (key == '2'):
				print(bcolors.GREEN+20*'-'+'*** Start Test application ***'+20*'-'+bcolors.ENDC)
				reset_and_start_application()

			headline()
			key = input("Select operation - ")

	print(bcolors.GREEN+20*'-'+'*** Quit firmware_flash script ***'+20*'-'+bcolors.ENDC)
	port_write_cmd = 'i2cset -y 1 0x20 0x12 0x00'
	os.system(port_write_cmd)


if __name__ == '__main__':
        main()

