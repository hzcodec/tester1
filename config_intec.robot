Resource  common.robot
Resource  unicorn.robot

*** Variables ***

# Define DAC properties
&{DAC_CH0_RANGE_0_10V}    Device=${DAC61408_DEVICE}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DACRANGE1}  Range=${DAC_RANGE_0V_p10V}  DAC=${DAC0}
&{DAC_CH0_OUT_8V0}    Device=${DAC61408_DEVICE}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DAC0}  Voltage=${8.0}
&{DAC_CH0_OUT_0V}    Device=${DAC61408_DEVICE}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DAC0}  Voltage=${0.0}

&{DAC_CH1_RANGE_0_10V}    Device=${DAC61408_DEVICE}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DACRANGE1}  Range=${DAC_RANGE_0V_p10V}  DAC=${DAC1}
&{DAC_CH1_OUT_4V0}    Device=${DAC61408_DEVICE}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DAC1}  Voltage=${4.0}
&{DAC_CH1_OUT_0V}    Device=${DAC61408_DEVICE}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DAC1}  Voltage=${0.0}

&{DAC_CH2_RANGE_0_10V}    Device=${DAC61408_DEVICE}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DACRANGE1}  Range=${DAC_RANGE_0V_p10V}  DAC=${DAC2}
&{DAC_CH2_OUT_6V0}    Device=${DAC61408_DEVICE}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DAC2}  Voltage=${6.0}
&{DAC_CH2_OUT_0V}    Device=${DAC61408_DEVICE}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DAC2}  Voltage=${0.0}

&{DAC_CH3_RANGE_0_10V}    Device=${DAC61408_DEVICE}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DACRANGE1}  Range=${DAC_RANGE_0V_p10V}  DAC=${DAC3}
&{DAC_CH3_OUT_2V0}    Device=${DAC61408_DEVICE}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DAC3}  Voltage=${2.0}
&{DAC_CH3_OUT_0V}    Device=${DAC61408_DEVICE}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DAC3}  Voltage=${0.0}



&{DAC_CH4_RANGE_0_5V}    Device=${DAC61408_DEVICE}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DACRANGE1}  Range=${DAC_RANGE_0V_p5V}  DAC=${DAC4}
&{DAC_CH4_OUT_2V5}    Device=${DAC61408_DEVICE}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DAC4}  Voltage=${2.5}

&{DAC_CH5_RANGE_0_5V}    Device=${DAC61408_DEVICE}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DACRANGE1}  Range=${DAC_RANGE_0V_p5V}  DAC=${DAC5}
&{DAC_CH5_OUT_2V5}    Device=${DAC61408_DEVICE}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DAC5}  Voltage=${2.5}

&{DAC_CH6_RANGE_0_5V}    Device=${DAC61408_DEVICE}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DACRANGE1}  Range=${DAC_RANGE_0V_p5V}  DAC=${DAC6}
&{DAC_CH6_OUT_2V5}    Device=${DAC61408_DEVICE}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DAC6}  Voltage=${2.5}

&{DAC_CH7_RANGE_0_5V}    Device=${DAC61408_DEVICE}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DACRANGE1}  Range=${DAC_RANGE_0V_p5V}  DAC=${DAC7}
&{DAC_CH7_OUT_2V5}    Device=${DAC61408_DEVICE}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DAC7}  Voltage=${2.5}
# ----------------------------------------------------------------------------------------------------------------------------------

# Define ADC properties
&{AD_NO_0}    Device=${AD4112_DEVICE_0}  SPI-addr=${NA}   Adc=${VIN_0}
&{AD_NO_1}    Device=${AD4112_DEVICE_0}  SPI-addr=${NA}   Adc=${VIN_1}
&{AD_NO_2}    Device=${AD4112_DEVICE_0}  SPI-addr=${NA}   Adc=${VIN_2}
&{AD_NO_3}    Device=${AD4112_DEVICE_0}  SPI-addr=${NA}   Adc=${VIN_3}
&{AD_NO_4}    Device=${AD4112_DEVICE_0}  SPI-addr=${NA}   Adc=${VIN_4}
&{AD_NO_5}    Device=${AD4112_DEVICE_0}  SPI-addr=${NA}   Adc=${VIN_5}
&{AD_NO_6}    Device=${AD4112_DEVICE_0}  SPI-addr=${NA}   Adc=${VIN_6}
&{AD_NO_7}    Device=${AD4112_DEVICE_0}  SPI-addr=${NA}   Adc=${VIN_7}
# ----------------------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------
# Define MCP23S17 instance 0, addr 1, port A properties, OUT
&{SPI_MCP_IOCON_HAEN_ADDR_0}     Device=${MCP23S17_DEVICE_0}  SPI-addr=${MCP23S17_ADDR_0}  Reg=${SPI_IOCON}
&{SPI_MCP_IOCON_HAEN_ADDR_1}     Device=${MCP23S17_DEVICE_0}  SPI-addr=${MCP23S17_ADDR_1}  Reg=${SPI_IOCON}
&{SPI_MCP_i1_a0_IOCON_HAEN}     Device=${MCP23S17_DEVICE_1}  SPI-addr=${MCP23S17_ADDR_0}  Reg=${SPI_IOCON}
# ----------------------------------------------------------------------------------------------------------------------------------

# Define generic AD4112
&{ADC_GET_ID_DEV_0}     Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${ID}
&{ADC_GET_ID_DEV_1}     Device=${AD4112_DEVICE_1}  SPI-addr=${SPI_ADDRESS_0}  Reg=${ID}
&{ADC_GAIN_DEV_0}     Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${GAIN}

&{ADC_SETUP_DEV_0}    Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${SETUPCON0}  Type=${UNI_POLAR}
&{ADC_MODE1_DEV_0}    Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${ADCMODE}
&{ADC_IFMODE_DEV_0}    Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${IFMODE}
&{ADC_GET_STATUS_DEV_0}    Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${STATUS}

&{ADC_SETUP_DEV_1}    Device=${AD4112_DEVICE_1}  SPI-addr=${SPI_ADDRESS_0}  Reg=${SETUPCON1}  Type=${BI_POLAR}
&{ADC_MODE1_DEV_1}    Device=${AD4112_DEVICE_1}  SPI-addr=${SPI_ADDRESS_0}  Reg=${ADCMODE}
&{ADC_IFMODE_DEV_1}    Device=${AD4112_DEVICE_1}  SPI-addr=${SPI_ADDRESS_0}  Reg=${IFMODE}
&{ADC_GET_STATUS_DEV_1}    Device=${AD4112_DEVICE_1}  SPI-addr=${SPI_ADDRESS_0}  Reg=${STATUS}
&{ADC_SETUP_DEV_1_5V_NEG}    Device=${AD4112_DEVICE_1}  SPI-addr=${SPI_ADDRESS_0}  Reg=${SETUPCON1}

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


*** Keywords ***
Config DIO ports
	Config MCP    ${SPI_MCP_IOCON_HAEN_ADDR_0}

	Config MCP port    ${DIO_0}    ${OUT}
	Config MCP port    ${DIO_1}    ${OUT}
	Config MCP port    ${DIO_2}    ${OUT}
	Config MCP port    ${DIO_3}    ${OUT}
	Config MCP port    ${DIO_4}    ${OUT}
	Config MCP port    ${DIO_5}    ${OUT}
	Config MCP port    ${DIO_6}    ${OUT}
	Config MCP port    ${DIO_7}    ${OUT}

	Config MCP port    ${DIO_8}    ${OUT}
	Config MCP port    ${DIO_9}    ${OUT}
	Config MCP port    ${DIO_10}   ${OUT}
	Config MCP port    ${DIO_11}   ${OUT}
	Config MCP port    ${DIO_12}   ${OUT}
	Config MCP port    ${DIO_13}   ${OUT}
	Config MCP port    ${DIO_14}   ${OUT}
	Config MCP port    ${DIO_15}   ${OUT}

	Config MCP    ${SPI_MCP_IOCON_HAEN_ADDR_1}

	Config MCP port    ${DIO_16}    ${OUT}
	Config MCP port    ${DIO_17}    ${OUT}
	Config MCP port    ${DIO_18}    ${OUT}
	Config MCP port    ${DIO_19}    ${OUT}

	Config MCP port    ${DIO_20}   ${OUT}
	Config MCP port    ${DIO_21}   ${OUT}
	Config MCP port    ${DIO_22}   ${OUT}
	Config MCP port    ${DIO_23}   ${OUT}

