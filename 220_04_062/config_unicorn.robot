Resource  common.robot

*** Variables ***
# ----------------------------------------------------------------------------------------------------------------------------------
&{SPI_MCP_i1_a0_IOCON_HAEN}     Device=${MCP23S17_DEVICE_1}  SPI-addr=${MCP23S17_ADDR_0}  Reg=${SPI_IOCON}
&{SPI_MCP_i1_a0_CONFIG_OPTO_A}     Device=${MCP23S17_DEVICE_1}  SPI-addr=${MCP23S17_ADDR_0}  Reg=${SPI_OPTO_A_IN}
&{SPI_MCP_i1_a0_CONFIG_OPTO_B}     Device=${MCP23S17_DEVICE_1}  SPI-addr=${MCP23S17_ADDR_0}  Reg=${SPI_OPTO_B_IN}
&{SPI_MCP_i0_a1_CONFIG_OPTO_B}     Device=${MCP23S17_DEVICE_0}  SPI-addr=${MCP23S17_ADDR_1}  Reg=${SPI_OPTO_B_OUT}

# ----------------------------------------------------------------------------------------------------------------------------------
# Define generic AD4112
&{ADC_GET_ID_DEV_0}     Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${ID}
&{ADC_GET_ID_DEV_1}     Device=${AD4112_DEVICE_1}  SPI-addr=${SPI_ADDRESS_0}  Reg=${ID}

# this one is in config_intec.robot
#&{ADC_SETUP_DEV_0}    Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${SETUPCON0}
#&{ADC_MODE1_DEV_0}    Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${ADCMODE}
#&{ADC_IFMODE_DEV_0}    Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${IFMODE}
#&{ADC_GET_STATUS_DEV_0}    Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${STATUS}

# this one is in config_intec.robot
#&{ADC_SETUP_DEV_1}    Device=${AD4112_DEVICE_1}  SPI-addr=${SPI_ADDRESS_0}  Reg=${SETUPCON0}
#&{ADC_MODE1_DEV_1}    Device=${AD4112_DEVICE_1}  SPI-addr=${SPI_ADDRESS_0}  Reg=${ADCMODE}
#&{ADC_IFMODE_DEV_1}    Device=${AD4112_DEVICE_1}  SPI-addr=${SPI_ADDRESS_0}  Reg=${IFMODE}
#&{ADC_GET_STATUS_DEV_1}    Device=${AD4112_DEVICE_1}  SPI-addr=${SPI_ADDRESS_0}  Reg=${STATUS}

# ----------------------------------------------------------------------------------------------------------------------------------
# Define AD4112, Device 0, Channel 3, 5V, 12V, 24V
&{ADC_CH3_DEV_0}    Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${CH3}
&{ADC_READ_VOLT_DEV_0_CH3}    Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DATA}  Type=${MEAS_VOLT}

# ----------------------------------------------------------------------------------------------------------------------------------
# Define AD4112, Device 1, Channel 4, 3.3VA
&{ADC_CH4_DEV_1}    Device=${AD4112_DEVICE_1}  SPI-addr=${SPI_ADDRESS_0}  Reg=${CH4}
&{ADC_READ_VOLT_DEV_1_CH4}    Device=${AD4112_DEVICE_1}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DATA}  Type=${MEAS_VOLT}

# ----------------------------------------------------------------------------------------------------------------------------------
# Define AD4112, Device 1, Channel 5, 3.3VD
&{ADC_CH5_DEV_1}    Device=${AD4112_DEVICE_1}  SPI-addr=${SPI_ADDRESS_0}  Reg=${CH5}
&{ADC_READ_VOLT_DEV_1_CH5}    Device=${AD4112_DEVICE_1}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DATA}  Type=${MEAS_VOLT}

# ----------------------------------------------------------------------------------------------------------------------------------
# Define AD4112, Device 0, Channel 6, 6VD
&{ADC_CH6_DEV_0}    Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${CH6}
&{ADC_READ_VOLT_DEV_0_CH6}    Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DATA}  Type=${MEAS_VOLT}

# ----------------------------------------------------------------------------------------------------------------------------------
# Define AD4112, Device 1, Channel 2, PP6V
&{ADC_CH2_DEV_1}    Device=${AD4112_DEVICE_1}  SPI-addr=${SPI_ADDRESS_0}  Reg=${CH2}
&{ADC_READ_VOLT_DEV_1_CH2}    Device=${AD4112_DEVICE_1}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DATA}  Type=${MEAS_VOLT}

# ----------------------------------------------------------------------------------------------------------------------------------
# Define AD4112, Device 1, Channel 0, AUX_PWR
&{ADC_CH0_DEV_1}    Device=${AD4112_DEVICE_1}  SPI-addr=${SPI_ADDRESS_0}  Reg=${CH0}
&{ADC_READ_VOLT_DEV_1_CH0}    Device=${AD4112_DEVICE_1}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DATA}  Type=${MEAS_VOLT}

# ----------------------------------------------------------------------------------------------------------------------------------
# Define AD4112, Device 1, Channel 1, USB_VBUS_1
&{ADC_CH1_DEV_1}    Device=${AD4112_DEVICE_1}  SPI-addr=${SPI_ADDRESS_0}  Reg=${CH1}
&{ADC_READ_VOLT_DEV_1_CH1}    Device=${AD4112_DEVICE_1}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DATA}  Type=${MEAS_VOLT}

# ----------------------------------------------------------------------------------------------------------------------------------
# Define AD4112, Device 1, Channel 6, 5VD_ISO
&{ADC_CH6_DEV_1}    Device=${AD4112_DEVICE_1}  SPI-addr=${SPI_ADDRESS_0}  Reg=${CH6}
&{ADC_READ_VOLT_DEV_1_CH6}    Device=${AD4112_DEVICE_1}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DATA}  Type=${MEAS_VOLT}

# ----------------------------------------------------------------------------------------------------------------------------------
# Define AD4112, Device 1, Channel 7, 5VD_NEG
&{ADC_CH7_DEV_1}    Device=${AD4112_DEVICE_1}  SPI-addr=${SPI_ADDRESS_0}  Reg=${CH7}
&{ADC_READ_VOLT_DEV_1_CH7}    Device=${AD4112_DEVICE_1}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DATA}  Type=${MEAS_VOLT}

# ----------------------------------------------------------------------------------------------------------------------------------
# Define AD4112, Device 0, Channel 7, OR_PWR
&{ADC_CH7_DEV_0}    Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${CH7}
&{ADC_READ_VOLT_DEV_0_CH7}    Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DATA}  Type=${MEAS_VOLT}

# ----------------------------------------------------------------------------------------------------------------------------------
# Define AD4112, Device 0, Channel 2, COM_P5VD_I 
&{ADC_CH2_DEV_0}    Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${CH2}
&{ADC_READ_VOLT_DEV_0_CH2}    Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DATA}  Type=${MEAS_VOLT}

# ----------------------------------------------------------------------------------------------------------------------------------
# Define AD4112, Device 0, Channel 0, HF_P8VD_I
&{ADC_CH0_DEV_0}    Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${CH0}
&{ADC_READ_VOLT_DEV_0_CH0}    Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DATA}  Type=${MEAS_VOLT}

# ----------------------------------------------------------------------------------------------------------------------------------
# Define AD4112, Device 0, Channel 4, HL_9V
&{ADC_CH4_DEV_0}    Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${CH4}
&{ADC_READ_VOLT_DEV_0_CH4}    Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DATA}  Type=${MEAS_VOLT}


# ----------------------------------------------------------------------------------------------------------------------------------
# Define AD4112, Device 0, Channel 1, Isolation test
&{ADC_CH1_DEV_0}    Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${CH1}
&{ADC_READ_VOLT_DEV_0_CH1}    Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DATA}  Type=${MEAS_VOLT}

# ----------------------------------------------------------------------------------------------------------------------------------
# Define AD4112, Device 0, Channel 5, V1_OUT - AI_05, LED test
&{ADC_CH5_DEV_0}    Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${CH5}
&{ADC_READ_VOLT_DEV_0_CH5}    Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DATA}  Type=${MEAS_VOLT}

&{PULLUP_PORT_A}    Device=${MCP23S17_DEVICE_1}  SPI-addr=${MCP23S17_ADDR_0}  Reg=${SPI_GPPUA}
&{PULLUP_PORT_B}    Device=${MCP23S17_DEVICE_1}  SPI-addr=${MCP23S17_ADDR_0}  Reg=${SPI_GPPUB}


*** Keywords ***
Config Opto in port A
	Config MCP    ${SPI_MCP_i1_a0_IOCON_HAEN}
	Config MCP    ${SPI_MCP_i1_a0_CONFIG_OPTO_A}

	#Config MCP port    ${SPI_GPIO_GPA0_A}    ${IN}
	#Config MCP port    ${SPI_GPIO_GPA1_A}    ${IN}
	#Config MCP port    ${SPI_GPIO_GPA2_A}    ${IN}
	#Config MCP port    ${SPI_GPIO_GPA3_A}    ${IN}
	#Config MCP port    ${SPI_GPIO_GPA4_A}    ${IN}
	#Config MCP port    ${SPI_GPIO_GPA5_A}    ${IN}
	#Config MCP port    ${SPI_GPIO_GPA6_A}    ${IN}
	#Config MCP port    ${SPI_GPIO_GPA7_A}    ${IN}
	Config MCP    ${PULLUP_PORT_A}

Config Opto in port B
	Config MCP    ${SPI_MCP_i1_a0_IOCON_HAEN}
	Config MCP    ${SPI_MCP_i1_a0_CONFIG_OPTO_B}

	#Config MCP port    ${SPI_GPIO_GPB0_A}    ${IN}
	#Config MCP port    ${SPI_GPIO_GPB1_A}    ${IN}
	#Config MCP port    ${SPI_GPIO_GPB2_A}    ${IN}
	#Config MCP port    ${SPI_GPIO_GPB3_A}    ${IN}
	#Config MCP port    ${SPI_GPIO_GPB4_A}    ${IN}
	#Config MCP port    ${SPI_GPIO_GPB5_A}    ${IN}
	#Config MCP port    ${SPI_GPIO_GPB6_A}    ${IN}
	#Config MCP port    ${SPI_GPIO_GPB7_A}    ${IN}
	Config MCP    ${PULLUP_PORT_B}

Config GPB0_C to GPB7_C
	Config MCP    ${SPI_MCP_IOCON_HAEN_ADDR_1}
	#Config MCP    ${SPI_MCP_i0_a1_CONFIG_OPTO_B}

	Config MCP port    ${GPB0_C}    ${OUT}
	Config MCP port    ${GPB1_C}    ${OUT}
	Config MCP port    ${GPB2_C}    ${OUT}
	Config MCP port    ${GPB3_C}    ${OUT}
	Config MCP port    ${GPB4_C}    ${OUT}
	Config MCP port    ${GPB5_C}    ${OUT}
	Config MCP port    ${GPB6_C}    ${OUT}
	Config MCP port    ${GPB7_C}    ${OUT}

