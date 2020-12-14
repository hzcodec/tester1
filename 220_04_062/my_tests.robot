*** Settings ***
Library   Dialogs
Library   DateTime

Resource  common.robot
Resource  config.robot
Resource  unicorn.robot

suite setup  Setup Suite
suite teardown  Teardown Suite

test setup  Setup Test
test teardown  Teardown Test

*** Variables ***
&{MCP_dev0_addr1}    Device=${MCP23S17_DEVICE_0}  SPI-addr=${MCP23S17_ADDR_1}  Reg=${SPI_IOCON}  Port=${DUMMY}  Mode=${DUMMY}
&{DAC1_RANGE_0_5V}    Device=${DAC61408_DEVICE}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DACRANGE1}  Range=${DAC_RANGE_0V_p5V}  DAC=${DAC1}

&{ADC_SETUP}    Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${SETUPCON0}
&{ADC_MODE1}    Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${ADCMODE}
&{ADC_CH6}    Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${CH6}
&{ADC_IFMODE}    Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${IFMODE}
&{ADC_READ_VOLT}    Device=${AD4112_DEVICE_0}  SPI-addr=${SPI_ADDRESS_0}  Reg=${DATA}  Type=${MEAS_VOLT}


*** Keywords ***
Setup Suite
	Log to console    *** Setup suite now
	Initialize interface and HW

Teardown Suite
	Log to console    *** Teardown suite now

Setup Test
	Log to console    *** Setup test now

Teardown Test
	Log to console    *** Teardown test now
	Set Relay1 and Relay2    ${OFF}

Initialize interface and HW
	${now}    Evaluate  '{dt:%A}, {dt:%B} {dt.day}, {dt.year}'.format(dt=datetime.datetime.now())    modules=datetime
	Log to Console    -------------------------- ${now} ------------------------
	Log to Console    ==============================================================================

	Initialize Interfaces
	Power Control  ${p_5eV}  ${ON}

	Config Unicorn HW

Set Relay1 and Relay2
	[Arguments]    ${mode}
	Relay Control  ${RELAY1}  ${mode}   # RL800
	Relay Control  ${RELAY2}  ${mode}   # RL801
	Sleep    1


*** Test Cases ***
Launch Relay test
	Set Relay1 and Relay2    ${ON}

Launch DAC test
	Log to console    Output 4.2 + 0.3V

	Config DAC  ${DAC1_RANGE_0_5V}
	Config DAC  ${DAC1_OUT_4V2}   # U408:5
	Sleep    2

	${DAC1_2V} =    Create Dictionary  Device=${DAC61408_DEVICE}
        ...                          	   SPI-addr=${SPI_ADDRESS_0}
	...    				   Reg=${DAC1}
	...			    	   Voltage=${2.0}

	Log to console    Output 2.0 + 0.3V
	Config DAC  ${DAC1_2V}
	Sleep    2

	${DEV_ID} =    Create Dictionary  Device=${DAC61408_DEVICE}
        ...                          	  SPI-addr=${SPI_ADDRESS_0}
	...    				  Reg=${DEVICE_ID}
	Config DAC  ${DEV_ID}

	Power Control  ${p_5eV}  ${OFF}

#Launch ADC test
#	${rv} =    Config ADC   ${ADC_READ_VOLT}
#	Should Be True  ${rv} > 2.8



# How to run standalone
#    python3 -m robot.run my_tests.robot
