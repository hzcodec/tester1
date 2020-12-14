import argparse
import os
import sys
import time
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

parser = argparse.ArgumentParser(description='Exclude test from Robot Framework run')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))


print('OK, server is running on local host')

def exit_app():
	print("Good Bye! See you later aligator. After a while crocodile")
	sys.exit()

def make_string_of_arguments(arg_list, marker):
	excluded_len = len(arg_list)

	i = 0
	# Mark every element with marker for the arguments.
	# This is so that main.py can extract the arguments.
	for ar in range(excluded_len):
		arg_list.insert(i, marker)
		i = i + 2
	
	excluded_arg_str = ""
	excluded_arg_str = ' '.join(arg_list) 

	return excluded_arg_str


# ----------------------------------------------------------------------------------------------
# Tags to include/exclude. Look into intec_tests.robot file for [Tags].
parser.add_argument('-e', nargs="+", type=str, default="", help="Exclude a test")
parser.add_argument('-i', nargs="+", type=str, default="", help="Include a test")
args = parser.parse_args()

excluded_rv = make_string_of_arguments(args.e, '1')
included_rv = make_string_of_arguments(args.i, '2')

while True:
	try:
		time.sleep(0.5)
		os.system('python3 main.py ' + excluded_rv + ' ' + included_rv)

		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes

		if data == b'Test ended by User':
			exit_app()

	except KeyboardInterrupt:
		exit_app()

# ----------------------------------------------------------------------------------------------
