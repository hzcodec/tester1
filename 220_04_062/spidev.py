# This is a dummy on since I'm running on host

class SpiDev:
	def __init__(self):
		#print('Init spidev')
		None

	def open(self, port, device):
		#print('Open port: {} for Device: {}'.format(port, device))
		None

	def mode(self, mode):
		print('Mode')

	def writebytes(self, data):
		#print('Write data: {}'.format(data))
		None

	def xfer2(self, a):
		# This is returning correct value for IOCON (HAEN bit is set)
		rv = [0x00, 0x00, 0x08]
		return rv

	def xfer3(self, a):
		# This is returning value for AD4112
		rv = [0x00, 0xf4, 0xc1, 0x0d, 0x06]
		return rv

	def xfer4(self, a):
		# This is returning value for ADC, device id
		rv = [0x00, 0x30, 0xd0]
		return rv

	def xfer5(self, a):
		# This is returning value for DAC, device id
		rv = [0x00, 0x09, 0x20]
		return rv

	def close(self):
		print('Close port')
