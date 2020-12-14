import datamatrix_to_ident
import datetime
import os
import re
import socket
import sys
import time

TEST_TO_RUN = 'intec_plc_tests.robot'
EXIT_MESSAGE = b'Test ended by User'
RUN_MESSAGE = b'Run application'
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
OUTPUT_DIR = "./logs/"

if sys.version_info[0] < 3:
    raise " *** Python 3 must be used ***"

import robot


class bcolors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    BGRN = '\033[1m'+'\033[92m'
    YELLOW = '\033[93m'
    BYEL = '\033[1m'+'\033[93m'
    RED = '\033[91m'
    BRED = '\033[1m'+'\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def launch_robot_test(output, variables, excluded_tags, included_tags):
		#excluded_tags = ["flash_sw", "dac_test"]
		#included_tags = ["flash_sw"]

		robot.run(TEST_TO_RUN, \
			loglevel='INFO', \
			exitonfailure=True, \
			noncritical="non-critical", \
			log=output+"_log", \
			variable=variables, \
			output=output, \
			report=output+"_report", \
			timestampoutputs=False, \
			include=included_tags, \
			exclude=excluded_tags)

def main():
	excluded_tags = []
	included_tags = []

	# create lists for the arguments
	for idx in range(len(sys.argv)-1):
		if sys.argv[idx+1] == '1':
			excluded_tags.append(sys.argv[idx+2])

		if sys.argv[idx+1] == '2':
			included_tags.append(sys.argv[idx+2])


	if not excluded_tags:
		print(bcolors.BGRN+'No "Exclude tags" are added'+bcolors.ENDC)
	else:
		print('Excluded_tags: {}{}{}'.format(bcolors.BRED, excluded_tags, bcolors.ENDC))

	if not included_tags:
		print(bcolors.BGRN+'No "Include tags" are added'+bcolors.ENDC)
	else:
		print('Included_tags: {}{}{}'.format(bcolors.BRED, included_tags, bcolors.ENDC))


	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	print(40*'-'+bcolors.BOLD+bcolors.YELLOW)
	scanned_datamatrix = input("Scan datamatrix (q = Quit app)--> ")

	if scanned_datamatrix != 'q':
		scanned_datamatrix = "00/5000100207/0PC1 1837337310 000025"
	else:
		None

	if scanned_datamatrix == 'q':
		sock.sendto(EXIT_MESSAGE, (UDP_IP, UDP_PORT))
		sys.exit()

	else:

		identity_command = datamatrix_to_ident.convert_scanned(scanned_datamatrix)
		variables = {'identity_command:'+identity_command}

		pos = identity_command.find('serial_number')
		print('Serial Number: {}'.format(identity_command[pos+15:pos+17]))

		print(bcolors.ENDC)

		output = OUTPUT_DIR + datamatrix_to_ident.convert_scanned(scanned_datamatrix, output_type=1) + \
		         "/" + datamatrix_to_ident.convert_scanned(scanned_datamatrix, output_type=1)


		launch_robot_test(output, variables, excluded_tags, included_tags)
		sock.sendto(RUN_MESSAGE, (UDP_IP, UDP_PORT))


if __name__ == '__main__':
        main()
