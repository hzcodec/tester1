import time

# --------------------------------------------------------------------------------
# Test functions used during development
# The Uxyz:ab numbers are refering to the component number on the schematic.
# Regarding the references, they are refering to CDIAG-200:01 00168, PB2.
# --------------------------------------------------------------------------------
def p_5Ve_test(obj):
	print(bcolors.BYEL+'5Ve test'+bcolors.ENDC)
	obj.power_control(p_5Ve, ON)  # MCP23017, addr=0, U304:25, RL203
	time.sleep(DELAY_1s)
	obj.power_control(p_5Ve, OFF)

def power_control_test(obj):
	print(bcolors.BYEL+'power_control_test, DC300V on'+bcolors.ENDC)
	obj.power_control(DC_300V, ON)           # U304:21
	time.sleep(DELAY_1s)

	print(bcolors.BYEL+'power_control_test, AC230V on'+bcolors.ENDC)
	obj.power_control(AC_230V, ON)           # U304:22
	time.sleep(DELAY_1s)

	print(bcolors.BYEL+'power_control_test, PROT_EARTH on'+bcolors.ENDC)
	obj.power_control(PROTECTED_EARTH, ON)   # U304:23
	time.sleep(DELAY_1s)

	print(bcolors.BYEL+'power_control_test, 24V on'+bcolors.ENDC)
	obj.power_control(p_24V, ON)             # U304:24
	time.sleep(DELAY_1s)

	print(bcolors.BYEL+'Turn OFF power'+bcolors.ENDC)
	obj.power_control(DC_300V, OFF)
	obj.power_control(AC_230V, OFF)
	obj.power_control(PROTECTED_EARTH, OFF)
	obj.power_control(p_5Ve, OFF)
	obj.power_control(p_24V, OFF)

def relay1_control_test(obj):
	print(bcolors.BYEL+'*** Relay 1 Control test ***'+bcolors.ENDC)
	obj.relay_control(RELAY1, ON)
	time.sleep(DELAY_1s)
	obj.relay_control(RELAY1, OFF)

def relay2_control_test(obj):
	print(bcolors.BYEL+'*** Relay 2 Control test ***'+bcolors.ENDC)
	obj.relay_control(RELAY2, ON)
	time.sleep(DELAY_1s)
	obj.relay_control(RELAY2, OFF)

def relay9_control_test(obj):
	print(bcolors.BYEL+'*** Relay 9 Control test ***'+bcolors.ENDC)
	obj.relay_control(RELAY9, ON)
	time.sleep(DELAY_1s)
	obj.relay_control(RELAY9, OFF)

def relay10_control_test(obj):
	print(bcolors.BYEL+'*** Relay 10 Control test ***'+bcolors.ENDC)
	obj.relay_control(RELAY10, ON)
	time.sleep(DELAY_1s)
	obj.relay_control(RELAY10, OFF)

#[TODO]: Check if this shall be removed
def ce_test(obj):
	#obj.spi0_ce0(DAC61408_DEVICE, 1)

	obj.spi0_ce0(AD4112_DEVICE_0, 1)
	obj.spi0_ce0(AD4112_DEVICE_0, 0)

	#obj.spi0_ce0(AD4112_DEVICE_1, 1)
	#obj.spi0_ce0(MCP23S17_DEVICE_0, 1)

	obj.spi0_ce0(MCP23S17_DEVICE_1, 1)
	obj.spi0_ce0(MCP23S17_DEVICE_1, 0)


def spi_port_inst_0_addr_0_B0_test(obj):
	# inst=0 addr=1, U301:1, GPB0, CS3

	obj.init_io_expander_i2c()
	obj.init_io_expander_spi()

	print(bcolors.BYEL+'Turn ON 5Ve'+bcolors.ENDC)
	obj.power_control(p_5Ve, ON)

	_MCP23S17_DEVICE_0 = '3'
	_MCP23S17_ADDR_0 = '0'
	_SPI_IOCON = '0x0a'
	_SPI_IODIRB = '0x01'
	_SPI_GPIOB = '0x13'
	_SPI_GPB0 = '0'
	_OUT = '0'
	_HI = '1'
	_LO = '0'

	print(bcolors.BYEL+'Set HAEN'+bcolors.ENDC)
	MCP_IOCON = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_IOCON}
	obj.config_mcp(MCP_IOCON)

	MCP_PORT = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_IODIRB, 'Port':_SPI_GPB0, 'Mode':_OUT}
	obj.config_mcp(MCP_PORT)

	print(bcolors.BYEL+'*** Set Port B0 high, U301:1'+bcolors.ENDC)
	MCP_PORT_HI = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_GPIOB, 'Port':_SPI_GPB0, 'Mode':_HI}
	obj.config_mcp(MCP_PORT_HI)

	time.sleep(2)

	print(bcolors.BYEL+'*** Set Port B0 low, U301:1'+bcolors.ENDC)
	MCP_PORT_LO = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_0, 'Reg':_SPI_GPIOB, 'Port':_SPI_GPB0, 'Mode':_LO}
	obj.config_mcp(MCP_PORT_LO)

	print(bcolors.BYEL+'Turn OFF 5Ve'+bcolors.ENDC)
	obj.power_control(p_5Ve, OFF)

def spi_port_inst_0_addr_1_A7_test(obj):
	# inst=0 addr=1, U302:28, GPA7, CS3

	obj.init_io_expander_i2c()
	obj.init_io_expander_spi()

	print(bcolors.BYEL+'Turn ON 5Ve'+bcolors.ENDC)
	obj.power_control(p_5Ve, ON)
	obj.power_control(p_24V, ON)
	time.sleep(DELAY_2s)

	_MCP23S17_DEVICE_0 = '3'
	_MCP23S17_ADDR_1 = '1'
	_SPI_IOCON_HAEN = '0x0a'
	_SPI_IODIRA = '0x00'
	_SPI_GPIOA = '0x12'
	_SPI_GPA7 = '7'
	_OUT = '0'
	_HI = '1'
	_LO = '0'

	print(bcolors.BYEL+'Set HAEN'+bcolors.ENDC)
	IOCON_HAEN = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_IOCON_HAEN}
	obj.config_mcp(IOCON_HAEN)

	PORT_7_OUT = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_IODIRA, 'Port':_SPI_GPA7, 'Mode':_OUT}
	obj.config_mcp(PORT_7_OUT)

	print(bcolors.BYEL+'*** Set Port A7 high, U302:28'+bcolors.ENDC)
	MCP_PORT_HI = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_GPIOA, 'Port':_SPI_GPA7, 'Mode':_HI}
	obj.config_mcp(MCP_PORT_HI)

	time.sleep(2)

	print(bcolors.BYEL+'*** Set Port A7 low, U302:28'+bcolors.ENDC)
	MCP_PORT_LO = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_GPIOA, 'Port':_SPI_GPA7, 'Mode':_LO}
	obj.config_mcp(MCP_PORT_LO)

	print(bcolors.BYEL+'Turn OFF 5Ve'+bcolors.ENDC)
	obj.power_control(p_24V, OFF)
	obj.power_control(p_5Ve, OFF)

def spi_port_inst_0_addr_1_A0_test(obj):
	# inst=0 addr=1, U302:21, GPA0, CS3

	obj.init_io_expander_i2c()
	obj.init_io_expander_spi()

	print(bcolors.BYEL+'Turn ON 5Ve'+bcolors.ENDC)
	obj.power_control(p_5Ve, ON)

	_MCP23S17_DEVICE_0 = '3'
	_MCP23S17_ADDR_1 = '1'
	_SPI_IOCON = '0x0a'
	_SPI_IODIRA = '0x00'
	_SPI_GPIOA = '0x12'
	_SPI_GPA0 = '0'
	_OUT = '0'
	_HI = '1'
	_LO = '0'

	print(bcolors.BYEL+'Set HAEN'+bcolors.ENDC)
	MCP_IOCON = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_IOCON}
	obj.config_mcp(MCP_IOCON)

	MCP_PORT = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_IODIRA, 'Port':_SPI_GPA0, 'Mode':_OUT}
	obj.config_mcp(MCP_PORT)

	print(bcolors.BYEL+'*** Set Port A0 high, U302:21'+bcolors.ENDC)
	MCP_PORT_HI = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_GPIOA, 'Port':_SPI_GPA0, 'Mode':_HI}
	obj.config_mcp(MCP_PORT_HI)

	time.sleep(2)

	print(bcolors.BYEL+'*** Set Port A0 low, U302:21'+bcolors.ENDC)
	MCP_PORT_LO = {'Device':_MCP23S17_DEVICE_0, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_GPIOA, 'Port':_SPI_GPA0, 'Mode':_LO}
	obj.config_mcp(MCP_PORT_LO)

	print(bcolors.BYEL+'Turn OFF 5Ve'+bcolors.ENDC)
	obj.power_control(p_5Ve, OFF)

def spi_port_inst_1_addr_0_A7_test(obj):
	# inst=1 addr=0, U300:21, GPA7, CS4

	obj.init_io_expander_i2c()
	obj.init_io_expander_spi()

	print(bcolors.BYEL+'Turn ON 5Ve'+bcolors.ENDC)
	obj.power_control(p_5Ve, ON)

	_MCP23S17_DEVICE_1 = '4'
	_MCP23S17_ADDR_1 = '0'
	_SPI_IOCON = '0x0a'
	_SPI_IODIRA = '0x00'
	_SPI_GPIOA = '0x12'
	_SPI_GPA7 = '7'
	_OUT = '0'
	_HI = '1'
	_LO = '0'

	print(bcolors.BYEL+'Set HAEN'+bcolors.ENDC)
	MCP_IOCON = {'Device':_MCP23S17_DEVICE_1, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_IOCON}
	obj.config_mcp(MCP_IOCON)

	MCP_PORT = {'Device':_MCP23S17_DEVICE_1, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_IODIRA, 'Port':_SPI_GPA7, 'Mode':_OUT}
	obj.config_mcp(MCP_PORT)

	print(bcolors.BYEL+'*** Set Port A0 high, U302:21'+bcolors.ENDC)
	MCP_PORT_HI = {'Device':_MCP23S17_DEVICE_1, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_GPIOA, 'Port':_SPI_GPA7, 'Mode':_HI}
	obj.config_mcp(MCP_PORT_HI)

	time.sleep(2)

	print(bcolors.BYEL+'*** Set Port A0 low, U302:21'+bcolors.ENDC)
	MCP_PORT_LO = {'Device':_MCP23S17_DEVICE_1, 'SPI-addr':_MCP23S17_ADDR_1, 'Reg':_SPI_GPIOA, 'Port':_SPI_GPA7, 'Mode':_LO}
	obj.config_mcp(MCP_PORT_LO)

	print(bcolors.BYEL+'Turn OFF 5Ve'+bcolors.ENDC)
	obj.power_control(p_5Ve, OFF)

def dac_ch1_0_5V_test(obj):
	print(bcolors.BYEL+'DAC1, range 0-5 V, Output=2.0 V'+bcolors.ENDC)
	obj.init_io_expander_i2c()
	obj.init_io_expander_spi()
	obj.power_control(p_5Ve, ON)

	obj.init_dac()

	_DEVICE_ID = '0x01'
	item3 = {'Device':DAC61408_DEVICE, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_DEVICE_ID}
	obj.config_dac(item3)

	_DACRANGE1 = '0x0c'
	_DAC_RANGE_0V_p5V = '0x0'
	_DAC1 = '0x15'
	item = {'Device':DAC61408_DEVICE, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_DACRANGE1, 'Range':_DAC_RANGE_0V_p5V, 'DAC': _DAC1}
	obj.config_dac(item)

	time.sleep(DELAY_05s)

	item2 = {'Device':DAC61408_DEVICE, 'SPI-addr':SPI_ADDRESS_0, 'Reg':'0x15', 'Voltage':'2.0'}
	obj.config_dac(item2)

	time.sleep(DELAY_3s)
	obj.power_control(p_5Ve, OFF)

def dac_ch1_0_10V_test(obj):
	print(bcolors.BYEL+'DAC1, range 0-10 V, Output=7.0 V'+bcolors.ENDC)
	obj.init_io_expander_i2c()
	obj.power_control(p_5Ve, ON)

	obj.init_io_expander_spi()
	obj.init_dac()

	_DACRANGE1 = '0x0c'
	_DAC_RANGE_0V_p10V = '0x1'
	_DAC1 = '0x15'
	item = {'Device':DAC61408_DEVICE, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_DACRANGE1, 'Range':_DAC_RANGE_0V_p10V, 'DAC': _DAC1}
	obj.config_dac(item)

	time.sleep(DELAY_1s)

	item2 = {'Device':DAC61408_DEVICE, 'SPI-addr':SPI_ADDRESS_0, 'Reg':'0x15', 'Voltage':'7.0'}
	obj.config_dac(item2)

	time.sleep(DELAY_3s)
	obj.power_control(p_5Ve, OFF)

def dac_ch1_0_20V_test(obj):
	print(bcolors.BYEL+'DAC1, range 0-20 V, Output=18.0 V'+bcolors.ENDC)
	obj.init_io_expander_i2c()
	obj.power_control(p_5Ve, ON)

	obj.init_io_expander_spi()
	obj.init_dac()

	_DACRANGE1 = '0x0c'
	_DAC_RANGE_0V_p20V = '0x2'
	_DAC1 = '0x15'
	item = {'Device':DAC61408_DEVICE, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_DACRANGE1, 'Range':_DAC_RANGE_0V_p20V, 'DAC': _DAC1}
	obj.config_dac(item)

	time.sleep(DELAY_1s)

	item2 = {'Device':DAC61408_DEVICE, 'SPI-addr':SPI_ADDRESS_0, 'Reg':'0x15', 'Voltage':'18.0'}
	obj.config_dac(item2)

	time.sleep(DELAY_3s)
	obj.power_control(p_5Ve, OFF)

def dac_ch1_and_ch2_0_5V_test(obj):
	print(bcolors.BYEL+'DAC CH1 and CH2, range 0-5 V'+bcolors.ENDC)
	obj.init_io_expander_i2c()
	obj.power_control(p_5Ve, ON)

	obj.init_io_expander_spi()
	obj.init_dac()

	_DACRANGE1 = '0x0c'
	_DAC_RANGE_0V_p5V = '0x0'
	_DAC1 = '0x15'
	_DAC2 = '0x16'

	# channel 1
	print(bcolors.BYEL+'DAC CH1 , Output=3.0 V'+bcolors.ENDC)
	item1 = {'Device':DAC61408_DEVICE, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_DACRANGE1, 'Range':_DAC_RANGE_0V_p5V, 'DAC': _DAC1}
	obj.config_dac(item1)
	time.sleep(DELAY_1s)
	item2 = {'Device':DAC61408_DEVICE, 'SPI-addr':SPI_ADDRESS_0, 'Reg':'0x15', 'Voltage':'3.0'}
	obj.config_dac(item2)

	# channel 2
	print(bcolors.BYEL+'DAC CH2 , Output=2.0 V'+bcolors.ENDC)
	item3 = {'Device':DAC61408_DEVICE, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_DACRANGE1, 'Range':_DAC_RANGE_0V_p5V, 'DAC': _DAC2}
	obj.config_dac(item3)
	time.sleep(DELAY_1s)
	item4 = {'Device':DAC61408_DEVICE, 'SPI-addr':SPI_ADDRESS_0, 'Reg':'0x16', 'Voltage':'2.0'}
	obj.config_dac(item4)

	time.sleep(DELAY_3s)
	obj.power_control(p_5Ve, OFF)

def adc_id_device_1_test(obj):
	obj.init_io_expander_i2c()
	obj.power_control(p_5Ve, ON)

	obj.init_io_expander_spi()
	obj.init_adc()

	_ID = '0x07'
	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_ID}
	obj.config_adc(item)

	time.sleep(0.2)

def adc_ch0_device_1_test(obj):
	_CH0 = '0x10'
	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_CH0}
	obj.config_adc(item)
	time.sleep(DELAY_01s)

	_SETUPCON0 = '0x20'
	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_SETUPCON0}
	obj.config_adc(item)
	time.sleep(DELAY_01s)

	_ADCMODE = '0x01'
	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_ADCMODE}
	obj.config_adc(item)

	_IFMODE = '0x02'
	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_IFMODE}
	obj.config_adc(item)

	_DATA = '0x04'
	_MEAS_VOLT = '1'
	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_DATA, 'Type':_MEAS_VOLT}
	rv = obj.config_adc(item)
	print(bcolors.BYEL+'Voltage in unicorn - {0:.1f}V'.format(rv)+bcolors.ENDC)

	_STATUS = '0x00'
	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_STATUS}
	obj.config_adc(item)

	time.sleep(1)
	obj.power_control(p_5Ve, OFF)

def adc_ch6_device_1_test(obj):
	print(bcolors.BYEL+'Device 1, Channel 6'+bcolors.ENDC)
	#obj.init_io_expander_i2c()
	#obj.power_control(p_5Ve, ON)

	#obj.init_io_expander_spi()
	#obj.init_adc()

	_CH6 = '0x16'
	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_CH6}
	obj.config_adc(item)
	time.sleep(DELAY_01s)

	_SETUPCON0 = '0x20'
	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_SETUPCON0}
	obj.config_adc(item)
	time.sleep(DELAY_01s)

	_ADCMODE = '0x01'
	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_ADCMODE}
	obj.config_adc(item)

	_IFMODE = '0x02'
	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_IFMODE}
	obj.config_adc(item)

	_DATA = '0x04'
	_MEAS_VOLT = '1'
	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_DATA, 'Type':_MEAS_VOLT}
	rv = obj.config_adc(item)
	print(bcolors.BYEL+'Voltage in unicorn - {0:.1f}V'.format(rv)+bcolors.ENDC)

	_STATUS = '0x00'
	item = {'Device':AD4112_DEVICE_1, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_STATUS}
	obj.config_adc(item)

	time.sleep(1)
	obj.power_control(p_5Ve, OFF)

def adc_id_device_0_test(obj):
	obj.init_io_expander_i2c()
	obj.power_control(p_5Ve, ON)

	obj.init_io_expander_spi()
	obj.init_adc()

	_ID = '0x07'
	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_ID}
	obj.config_adc(item)

	time.sleep(0.2)

def adc_ch0_device_0_test(obj):
	print(bcolors.BYEL+'Device 0, Channel 0'+bcolors.ENDC)

	_CH0 = '0x10'
	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_CH0}
	obj.config_adc(item)
	time.sleep(DELAY_01s)

	_SETUPCON0 = '0x20'
	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_SETUPCON0}
	obj.config_adc(item)
	time.sleep(DELAY_01s)

	_ADCMODE = '0x01'
	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_ADCMODE}
	obj.config_adc(item)

	_IFMODE = '0x02'
	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_IFMODE}
	obj.config_adc(item)

	_DATA = '0x04'
	_MEAS_VOLT = '1'
	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_DATA, 'Type':_MEAS_VOLT}
	rv = obj.config_adc(item)
	print(bcolors.BYEL+'Voltage in unicorn - {0:.1f}V'.format(rv)+bcolors.ENDC)

	_STATUS = '0x00'
	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_STATUS}
	obj.config_adc(item)

	time.sleep(1)
	obj.power_control(p_5Ve, OFF)

def adc_ch6_device_0_test(obj):
	_CH6 = '0x16'
	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_CH6}
	obj.config_adc(item)
	time.sleep(DELAY_01s)

	_SETUPCON0 = '0x20'
	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_SETUPCON0}
	obj.config_adc(item)
	time.sleep(DELAY_01s)

	_ADCMODE = '0x01'
	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_ADCMODE}
	obj.config_adc(item)

	_IFMODE = '0x02'
	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_IFMODE}
	obj.config_adc(item)

	_DATA = '0x04'
	_MEAS_VOLT = '1'
	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_DATA, 'Type':_MEAS_VOLT}
	rv = obj.config_adc(item)
	print(bcolors.BYEL+'Voltage in unicorn - {0:.1f}V'.format(rv)+bcolors.ENDC)

	_STATUS = '0x00'
	item = {'Device':AD4112_DEVICE_0, 'SPI-addr':SPI_ADDRESS_0, 'Reg':_STATUS}
	obj.config_adc(item)

	time.sleep(1)
	obj.power_control(p_5Ve, OFF)
