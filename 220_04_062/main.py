import sys
import os
import time
import datetime
import re
import random

TEST_TO_RUN = 'my_tests.robot'


if sys.version_info[0] < 3:
    raise " *** Python 3 must be used ***"

import robot


class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main():

	while(1):
		date_string = str(datetime.datetime.now())
		output = '../Logs/DUT_NAME'+'/'+date_string+'/PROJECT_NAME'

		print(40*'-'+bcolors.BOLD+bcolors.YELLOW)
		prod_label = str(input("Scan datamatrix --> "))
		print(bcolors.ENDC)

		if prod_label == "Test ended by User":
			break

		robot.run(TEST_TO_RUN, \
			loglevel='INFO', \
			exitonfailure=True, \
			noncritical="non-critical", \
			log=output+"_log", \
			output=output, \
			report=output+"_report", \
			timestampoutputs=True, \
			exclude="manual_test")
				

if __name__ == '__main__':
        main()
