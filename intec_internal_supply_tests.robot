*** Settings ***
Library   Dialogs

Resource  220_04_062/common.robot
Resource  220_04_062/unicorn.robot
Resource  config_intec.robot


*** Variables ***


*** Keywords ***
Default Setup Device 0
	Config ADC   ${ADC_SETUP_DEV_0}
	Config ADC   ${ADC_MODE1_DEV_0}
	Config ADC   ${ADC_IFMODE_DEV_0}

Default Setup Device 1
	Config ADC   ${ADC_SETUP_DEV_1}
	Config ADC   ${ADC_MODE1_DEV_1}
	Config ADC   ${ADC_IFMODE_DEV_1}

Default Setup Device 1 5V_NEG
	Config ADC   ${ADC_SETUP_DEV_1_5V_NEG}
	Config ADC   ${ADC_MODE1_DEV_1}
	Config ADC   ${ADC_IFMODE_DEV_1}

Setup ADC for 3V3A Voltage Check
	Config ADC   ${ADC_GET_ID_DEV_1}
	Config ADC   ${ADC_CH4_DEV_1}
	Default Setup Device 1

Setup ADC for 3V3D Voltage Check
	Config ADC   ${ADC_GET_ID_DEV_1}
	Config ADC   ${ADC_CH5_DEV_1}
	Default Setup Device 1

Setup ADC for 6VD Voltage Check
	Config ADC   ${ADC_GET_ID_DEV_0}
	Config ADC   ${ADC_CH6_DEV_0}
	Default Setup Device 0

Setup ADC for PP6V Voltage Check
	Config ADC   ${ADC_GET_ID_DEV_1}
	Config ADC   ${ADC_CH2_DEV_1}
	Default Setup Device 1

Setup ADC for AUX Voltage Check
	Config ADC   ${ADC_GET_ID_DEV_1}
	Config ADC   ${ADC_CH0_DEV_1}
	Default Setup Device 1

Setup ADC for USB_VBUS Voltage Check
	Config ADC   ${ADC_GET_ID_DEV_1}
	Config ADC   ${ADC_CH1_DEV_1}
	Default Setup Device 1

Setup ADC for 5VD_ISO Voltage Check
	Config ADC   ${ADC_GET_ID_DEV_1}
	Config ADC   ${ADC_CH6_DEV_1}
	Default Setup Device 1

Setup ADC for 5VD_NEG Voltage Check
	Config ADC   ${ADC_GET_ID_DEV_1}
	Config ADC   ${ADC_CH7_DEV_1}
	Default Setup Device 1

Setup ADC for OR_PWR Voltage Check
	Config ADC   ${ADC_GET_ID_DEV_0}
	Config ADC   ${ADC_CH7_DEV_0}
	Default Setup Device 0

Setup ADC for COM_P5VD_I Voltage Check
	Config ADC   ${ADC_GET_ID_DEV_0}
	Config ADC   ${ADC_CH2_DEV_0}
	Default Setup Device 0

Setup ADC for HF_P8VD_I Voltage Check
	Config ADC   ${ADC_GET_ID_DEV_0}
	Config ADC   ${ADC_CH0_DEV_0}
	Default Setup Device 0

Setup ADC for HL_9V Voltage Check
	Config ADC   ${ADC_GET_ID_DEV_0}
	Config ADC   ${ADC_CH4_DEV_0}
	Default Setup Device 0

3V3A Incorrect
	[Arguments]  ${rv}
	Log to Console    *** 3V3 Analog is either to low or high
	Should Be True  ${rv} > 3.0 and ${rv} < 3.8

HL 9V Incorrect
	[Arguments]  ${rv}
	Log to Console    *** HL 9V is either to low or high
	Should Be True  ${rv} > 8.2 and ${rv} < 9.6

Test 3V3A
	Setup ADC for 3V3A Voltage Check
	Sleep    ${DELAY_05s}

	${rv} =    Config ADC   ${ADC_READ_VOLT_DEV_1_CH4}
	#Run Keyword If  ${rv} > 3.8 or ${rv} < 3.0   3V3A Incorrect  ${rv}
	Sleep    ${DELAY_05s}

Test HL_9V
	Setup ADC for HL_9V Voltage Check
	Sleep    ${DELAY_05s}

	${rv} =    Config ADC   ${ADC_READ_VOLT_DEV_0_CH4}
	#Run Keyword If  ${rv} > 9.6 or ${rv} < 8.2   HL 9V Incorrect  ${rv}
	Sleep    ${DELAY_05s}

