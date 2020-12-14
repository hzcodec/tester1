*** Settings ***
Library   Dialogs
Library   DateTime
Library   firmware_flash_plc
Library   serie_com

Resource  220_04_062/common.robot
Resource  220_04_062/config_unicorn.robot
Resource  220_04_062/unicorn.robot

Resource  config_intec.robot
Resource  intec_power_supply_tests.robot
Resource  intec_internal_supply_tests.robot

suite setup  Setup Suite
suite teardown  Teardown Suite

*** Variables ***
${result}    "1"
${expv1}    235    # should be 234 (0xea), but needle is not connected
${expv2}    245    # 0xf5
${expv3}    170    # 0xaa
${expv4}    213    # 0x55


*** Keywords ***
Setup Suite
	# Check that adaptor board is aligned with Robot tests
	Read ID file
	Initialize interface and HW
	Check Lid

Teardown Suite
	Set MCP port   ${DIO_7}    ${LOW}  # 24V OFF to DUT
	Turn Off 24V and 5Ve
	Power Control  ${L1}  ${OFF}

Read ID file
	${rv} =    Read Identification File
	Run Keyword If    not ${rv}   Fatal Error

Check Lid
	Check if lid is Closed
	Sleep    ${DELAY_02s}

Initialize interface and HW
	${now}  Evaluate  '{dt:%A}, {dt:%B} {dt.day}, {dt.year}, {dt.hour}:{dt.minute}'.format(dt=datetime.datetime.now())  modules=datetime
	Log to Console    ------------------------ ${now} -----------------
	Log to Console    ==============================================================================

	Initialize Interfaces
	Log to Console    Configure user defined DIO ports
	Config DIO ports


*** Test Cases ***
# -------------------------------------------------------------------------------------------------
# Power supply tests
# -------------------------------------------------------------------------------------------------
Check 5V
	[Tags]    pwr_test    pwr_supply    pwr_5V

	# setup mux/demux 
	Setup MUX_V2 for Voltage Check   ${CHECK_5V}

	# Setup ADC, Read analog input - It's-It U930A:1 AI_03 (J2:12) - Unicorn 1AI_1_N, VIN3 U405:28
	Setup ADC CH3 for Voltage Check

	${rv} =    Config ADC   ${ADC_READ_VOLT_DEV_0_CH3}
	#Run Keyword If  ${rv} > 5.3 or ${rv} < 4.5   5V Incorrect  ${rv}

	Sleep    ${DELAY_05s}
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Internal power supply tests
# -------------------------------------------------------------------------------------------------
Internal Power Supply Test
	[Tags]    pwr_test   int_pwr    ext_pwr


	Set MCP port   ${DIO_8}    ${LOW}   # Current limit to 115 mA
	Set MCP port   ${DIO_7}    ${HIGH}  # 24V ON to DUT
	Sleep    ${DELAY_05s}

	# Device 0
	Test HL_9V

	# Device 1
	Test 3V3A
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Firmware flash
# -------------------------------------------------------------------------------------------------
Flash PLC
	[Tags]    flash_plc

	Set MCP port   ${DIO_8}    ${LOW}   # Current limit to 115 mA
	Set MCP port   ${DIO_7}    ${HIGH}  # 24V ON to DUT

	Init DAC
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# LED test
# -------------------------------------------------------------------------------------------------
Debug LED test
	[Documentation]    Visual check is needed for Debug LED test
	[Tags]    led_test    led_dbg

	Red LED Test
	Green LED Test
	Yellow LED Test

Heater OK LED test
	[Documentation]    Visual check is needed for Heater OK_LED test
	[Tags]    led_test    led_ok

	He OK all LED Test
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# PLC Analog inputs
# -------------------------------------------------------------------------------------------------
PLC Analog input test
	[Tags]    ana_test

	#Log to Console    *** version
	#Sleep    ${DELAY_05s}
	#Get Version
	#Sleep    ${DELAY_05s}

	Log to Console    *** dev id
	${DEV_ID} =    Create Dictionary  Device=${DAC61408_DEVICE}
        ...                          	  SPI-addr=${SPI_ADDRESS_0}
	...    				  Reg=${DEVICE_ID}
	Config DAC  ${DEV_ID}
	Sleep    ${DELAY_05s}

        #${STATUS} =    Create Dictionary  Device=${DAC61408_DEVICE}
        #...                               SPI-addr=${SPI_ADDRESS_0}
        #...                               Reg=${DAC_STATUS}
        #Config DAC  ${STATUS}
	#Sleep    ${DELAY_05s}

	Log to Console    *** 1st
	Config DAC    ${DAC_CH0_RANGE_0_10V}
	Sleep    ${DELAY_05s}
	Config DAC    ${DAC_CH0_OUT_8V0}
	Sleep    ${DELAY_05s}

	Log to Console    *** 2nd
	#Config DAC    ${DAC_CH1_RANGE_0_10V}
	Sleep    ${DELAY_05s}
	Config DAC    ${DAC_CH1_OUT_4V0}
	Sleep    ${DELAY_05s}

	Log to Console    *** 3rd
	#Config DAC    ${DAC_CH2_RANGE_0_10V}
	Sleep    ${DELAY_05s}
	Config DAC    ${DAC_CH2_OUT_6V0}
	Sleep    ${DELAY_05s}

	Log to Console    *** 4th
	#Config DAC    ${DAC_CH3_RANGE_0_10V}
	Sleep    ${DELAY_05s}
	Config DAC    ${DAC_CH3_OUT_2V0}
	Sleep    ${DELAY_05s}

	${rv} =   Read Analog In
	Should be True   ${rv}
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# PLC Digital Output test
# -------------------------------------------------------------------------------------------------
PLC Digital Output LoCurr Test
	[Tags]    plc_test   plc_loc

	Low Current Test 1
	${rv} =  READ MCP port  ${SPI_READ_B}
	${expected_value} =   Convert To Integer  ${expv1} 
	Should be Equal    ${rv[2]}    ${expected_value}  

	Low Current Test 2
	${rv} =  READ MCP port  ${SPI_READ_B}
	${expected_value} =   Convert To Integer  ${expv2} 
	Should be Equal    ${rv[2]}    ${expected_value}  

PLC Digital Output HiCurr Test
	[Tags]    plc_test   plc_hic

	High Current Test 1
	${rv} =  READ MCP port  ${SPI_READ_A}
	${expected_value} =   Convert To Integer  ${expv3}
	Should be Equal    ${rv[2]}    ${expected_value}

	High Current Test 2
	${rv} =  READ MCP port  ${SPI_READ_A}
	${expected_value} =   Convert To Integer  ${expv4}
	Should be Equal    ${rv[2]}    ${expected_value}

	Sleep    ${DELAY_05s}
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# PLC Digital Input test
# -------------------------------------------------------------------------------------------------
PLC Digital Input Test
	[Tags]    plc_test   plc_in

	#Sleep    ${DELAY_05s}
	#Get Version
	#Sleep    ${DELAY_05s}

	Log to Console   *** DI test 1
	#Set MCP port   ${GPB0_C}    ${HIGH}   # DI1
	#Set MCP port   ${GPB2_C}    ${HIGH}   # DI3
	#Set MCP port   ${GPB4_C}    ${HIGH}   # DI5
	#Set MCP port   ${GPB6_C}    ${HIGH}   # DI7
	Set GPB_C port  ${0xaa}

	#Sleep    ${DELAY_05s}
	Log to Console   *** DI test 1 done

	${rv} =  Get DI 1 to 7    ${1}
	Should be True   ${rv}

	Log to Console   *** DI test 2
	#Set MCP port   ${GPB0_C}    ${LOW}   # DI1
	#Set MCP port   ${GPB2_C}    ${LOW}   # DI3
	#Set MCP port   ${GPB4_C}    ${LOW}   # DI5
	#Set MCP port   ${GPB6_C}    ${LOW}   # DI7
	#Set MCP port   ${GPB1_C}    ${HIGH}  # DI2
	#Set MCP port   ${GPB3_C}    ${HIGH}  # DI4
	#Set MCP port   ${GPB5_C}    ${HIGH}  # DI6
	Set GPB_C port  ${0x55}

	#Sleep    ${DELAY_05s}
	Log to Console   *** DI test 2 done

	${rv} =  Get DI 1 to 7    ${2}
	Should be True   ${rv}
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
Set identity
	[Tags]    set_id

	Log    ${identity_command}    console=true
	Log    Pass    console=true

	Set Identity    ${identity_command}
# -------------------------------------------------------------------------------------------------
