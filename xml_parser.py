# The script is parsing the "output.xml"-file and printing out the ports mode.
# I.e whether they are input or output.
#
# N.B! At startup all ports are by default declared as input. If the user does not
# declare the port as input this will not show up in the list.

# Now, reading and understanding the inner details of what this code is doing,
# I would'nt say it's supercalifragilisticexpialidocious. However it is doing
# its job rather well.

# Disclaimer: If you use this and you blow up your board, computer, office or
# even the Earth, I wont take any responsibility.

MCP23S17_DEVICE_0 = 3
MCP23S17_DEVICE_1 = 4
SPI_NO_OF_PORTS = 47  # 0 - 47 => 48 ports

class bcolors:
    GREEN = '\033[92m'
    BGREEN = '\033[1m' + '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BRED = '\033[1m' + '\033[91m'
    YELLOW = '\033[93m'
    BYEL = '\033[1m' + '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def search_string_in_file(file_name, string_to_search):

	line_number = 0
	list_of_results = []

	with open(file_name, 'r') as read_obj:
		for line in read_obj:

			line_number += 1
			if string_to_search in line:
				list_of_results.append((line_number, line.rstrip()))

	return list_of_results

def get_name_of_port(device, spi_addr, reg, port):
	#print('get_name: {}, spi_addr: {}, reg: {}, port: {}'.format(device, spi_addr, reg, port))

	if device == 3 and spi_addr == '0' and reg == '0x00':
		name = 'DIO_' + port

	elif device == 3 and spi_addr == '0' and reg == '0x01':
		name = 'DIO_' + str(int(port) + 8)

	elif device == 3 and spi_addr == '1' and reg == '0x00':
		name = 'DIO_' + str(int(port) + 16)

	elif device == 3 and spi_addr == '1' and reg == '0x01':
		name = 'GPB' + port + '_C'

	elif device == 4 and spi_addr == '0' and reg == '0x00':
		name = 'SPI_GPIO_GPA' + port + '_A'
                                          	
	elif device == 4 and spi_addr == '0' and reg == '0x01':
		name = 'SPI_GPIO_GPB' + port + '_A'

	else:
		name = 'Nobody'

	return name

def extract_info(rv):
	pos = rv[idx][1].find('Device')
	device = int(rv[idx][1][pos+10:pos+11])
	spi_addr = rv[idx][1][pos+27:pos+28]

	if device == MCP23S17_DEVICE_1 and spi_addr == '0':
		col = bcolors.BLUE

	elif device == MCP23S17_DEVICE_0 and spi_addr == '0':
		col = bcolors.BYEL

	else:
		col = bcolors.BGREEN

	reg = rv[idx][1][pos+39:pos+43]
	port = rv[idx][1][pos+55:pos+56]

	mode = rv[idx][1][pos+68:pos+69]

	if mode == '0':
		mode_str = 'OUT'
	else:
		mode_str = 'IN'

	rv = get_name_of_port(device, spi_addr, reg, port)
	print('{}Instance: {}, SPI-addr: {}, Reg: {}, Port: {}, Mode: {} - {}{} '.format(col, device-3, spi_addr, reg, port, mode_str, rv, bcolors.ENDC))


# =====================================================================================
# main
# =====================================================================================

rv = search_string_in_file('output.xml', 'MCP23017')
first_idx = rv[0][0]
second_idx = rv[1][0]

rv2 = search_string_in_file('output.xml', '(i2c) Direction')

print('   --- (i2c) MCP23017, addr=0 ---')
for p in rv2:
	if p[0] < second_idx:
		pos = p[1].index('Direction')
		pos2 = p[1].index(', Dir')

		if p[1][pos:pos+15] == 'Direction PortA':
			col = bcolors.BYEL	
		else:
			col = bcolors.BGREEN
		print(col+p[1][pos:pos2]+bcolors.ENDC)


print('\n   --- (i2c) MCP23017, addr=1 ---')
for p in rv2:
	if p[0] > second_idx:
		pos = p[1].index('Direction')
		pos2 = p[1].index(', Dir')

		if p[1][pos:pos+15] == 'Direction PortA':
			col = bcolors.BYEL	
		else:
			col = bcolors.BGREEN

		print(col+p[1][pos:pos2]+bcolors.ENDC)


print('\n           --- (spi) MCP23S17, Port A ---')
rv = search_string_in_file('output.xml', 'IODIRA')
for idx in range (SPI_NO_OF_PORTS):
	try:
		extract_info(rv)
	except:
		None

print('\n           --- (spi) MCP23S17, Port B ---')
rv = search_string_in_file('output.xml', 'IODIRB')
for idx in range (SPI_NO_OF_PORTS):
	try:
		extract_info(rv)
	except:
		None

