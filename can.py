#!/usr/bin/env python3

import subprocess
from robot.api import logger

def setup_can():
    if can0_exists():
        return "Can initialized"

    logger.console("Can not initialized, setup with:\n" \
    "sudo ip link set up can0 type can bitrate 1000000 restart-ms 100")
    return "Can not initialized"

def read_heartbeat():
    logger.console("\n")
    command = ('timeout 2 candump can0')

    logger.info(command)
    logger.console(command)

    result = subprocess.Popen(command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True)

    out, err = result.communicate()
    logger.info(out)
    logger.console(out)
    logger.console("\n")
    out_str = str(out)

    if "7F" in out_str:
        return True
    else:
        return False

def can0_exists():
    logger.console("\n")
    command = ('ifconfig')

    logger.info(command)
    logger.console(command)

    result = subprocess.Popen(command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True)

    out, err = result.communicate()
    logger.info(out)
    logger.console(out)
    logger.console("\n")
    out_str = str(out)

    if "can0" in out_str:
        return True
    else:
        return False


def main():
	rv = can0_exists()
	print('CAN0 exists: {}'.format(rv))

	rv = read_heartbeat()
	print('Heartbeat: {}'.format(rv))


if __name__ == '__main__':
        main()
