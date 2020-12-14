# pylint: disable=invalid-name
# pylint: disable=mixed-indentation
# pylint: disable=wrong-import-order

from robot.api import logger
from robot.utils.asserts import assert_equal, assert_not_none, assert_true
import can.interfaces
import canopen
import time


class CANopen:

	def __init__(self):
		self._active_node = None
		self._bitrate = None
		self._bustype = None
		self._channel = None
		self._network = canopen.Network()  # Create one network per CAN bus.
		self._od_file = None

	def connect_to_can_bus(self, bustype, channel, bitrate):
		try:
			self._network.connect(bustype=bustype, channel=channel, bitrate=bitrate)
			self._bustype = bustype
			self._channel = channel
			self._bitrate = bitrate
		except OSError as err:
			logger.error('Failed connecting to can bus. OSError: {}'.format(err))

	def scan_for_present_can_nodes(self):
		try:
			_node_id = None
			# This will attempt to read an SDO from nodes 1 - 127
			self._network.scanner.search()
			# We may need to wait a short while here to allow all nodes to respond
			time.sleep(0.05)
			if len(self._network.scanner.nodes) > 0:
				for node_id in self._network.scanner.nodes:
					logger.info('{} node with NodeID {} on the network'.format(len(self._network.scanner.nodes), node_id))
					_node_id = node_id
			else:
				logger.info('{} nodes on the network'.format(len(self._network.scanner.nodes)))
			return _node_id
		except RuntimeError:
			logger.error('Not connected to any CAN bus.')
		except can.CanError:
			logger.error('CAN error')

	# Object Dictionary / EDS-file
	def set_object_dictionary(self, od):
		self._od_file = od
		assert_true(self._od_file, "Can't find {} object dictionary file".format(self._od_file))
		logger.info('Object Dictionary is set to: {}'.format(self._od_file))

	# Select nodes with corresponding object dictionary file, and add the node to the network
	def select_can_node(self):
		_node_id = self.scan_for_present_can_nodes()
		self._active_node = self._network.add_node(_node_id, self._od_file)
		assert_not_none(self._active_node, 'No node has been selected')
		assert_true(self._od_file, "Can't find {} object dictionary file".format(self._od_file))

	def get_current_nmt_state(self):
		logger.info('Current NMT state is: {} '.format(self._active_node.nmt.state))
		return self._active_node.nmt.state

	def set_nmt_state(self, requested_state):
		logger.info('Requested NMT state: {}'.format(requested_state))
		assert_not_none(self._active_node, 'No node has been selected')
		state = requested_state.upper()  # Only uppercase letters are accepted
		self._active_node.nmt.state = state
		self._active_node.nmt.wait_for_heartbeat()  # To confirm the NMT command, wait for response
		assert_equal(self.get_current_nmt_state(), state)

	# Read a variable using SDO
	def sdo_read(self, index, subindex=0):
		assert_not_none(self._active_node, 'No node has been selected')
		if isinstance(index, str):
			index = int(index, 16)  # Convert string to 16-base integer
		try:
			if subindex == 0:
				logger.info('Read SDO: {}. Value: {:04x}'.format(hex(index), self._active_node.sdo[index].raw))
				return self._active_node.sdo[index].raw
			else:
				logger.info('Read SDO: {}:{}. Value: {:04x}'.format(hex(index), bin(subindex), self._active_node.sdo[index][subindex].raw))
				return self._active_node.sdo[index][subindex].raw
		except canopen.sdo.exceptions.SdoAbortedError:
			logger.error('Resource not available')
		except canopen.sdo.exceptions.SdoCommunicationError:
			logger.error('No or unexcpected response from slave')

	# Write a variable using SDO
	def sdo_write(self, value, index, subindex=0):
		assert_not_none(self._active_node, 'No node has been selected')
		if isinstance(index, str):
			index = int(index, 16)  # Convert string to 16-base integer
		try:
			if subindex == 0:
				logger.info('Write SDO: {}. Value: {:04x}'.format(hex(index), value))
				self._active_node.sdo[index].raw = value
				assert_equal(self._active_node.sdo[index].raw, value)
			else:
				logger.info('Write SDO: {}:{}. Value: {:04x}'.format(hex(index), bin(subindex), value))
				self._active_node.sdo[index][subindex].raw = value
				assert_equal(self._active_node.sdo[index][subindex].raw, value)
		except canopen.sdo.exceptions:
			logger.error('Failed writing to SDO.')

	def pdo_readall(self):
		assert_not_none(self._active_node, 'No node has been selected')
		self._active_node.pdo.read()

	# Read TPDO Map object at number [1-4]
	def tpdo_read(self, number):
		assert_not_none(self._active_node, 'No node has been selected')
		if number < 1 or number > 4:
			logger.warn('PDO Map number out of range. Can not publish TPDO object.')
		else:
			self._active_node.tpdo[number].read()

	# Read RPDO Map object at number [1-4]
	def rpdo_read(self, number):
		assert_not_none(self._active_node, 'No node has been selected')
		if number < 1 or number > 4:
			logger.warn('PDO Map number out of range. Can not publish RPDO object.')
		else:
			self._active_node.rpdo[number].read()

	def disconnect_from_can_bus(self):
		logger.info('Disconnecting {} from can bus.'.format(self._channel))
		self._channel = None
		self._active_node = None
		self._network.disconnect()


def main():
	print('This line is here for debugging purpose only.')


if __name__ == '__main__':
	main()
