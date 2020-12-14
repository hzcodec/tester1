*** Settings ***
Library   unicorn
Library   Dialogs

Resource  common.robot
Resource  config_unicorn.robot

*** Variables ***
${index}   0

*** Keywords ***
Invalid Selection
	Log To Console    *** Invalid Selection. Use 'ON' or 'OFF'

Initialize Interfaces
	Log to Console    *** Setup I2C and SPI interfaces
	Init IO Expander I2C
	Init IO Expander SPI

	Power Control  ${p_5Ve}  ${ON}
	Power Control  ${p_24V}  ${ON}

	Log to Console    Configure Predefined ports, 8x OPTO out and 16x OPTO in
	Config Opto in port A
	Config Opto in port B
	Config GPB0_C to GPB7_C

	Sleep    ${DELAY_02s}

Lid is Open
	Log to Console    ******************************************************
	Log to Console    *** Lid is Open. Must be closed before test starts ***
	Log to Console    ******************************************************

Config DAC61408
	Init DAC

Check if lid is Closed
	${rv} =    Read Closed

	Run Keyword if   ${rv} == 0  Lid is Open
	Run Keyword If    not ${rv}   Fatal Error

	Log to Console    Lid is locked!
	# Dra signalen L1_1, GPA5
	Power Control  ${L1}  ${ON}

	# Kolla S3 skall vara hög => 230V ...
	#[TODO]: Detta behöver pollas/trådas någonstans
	# S3 = 0 innebär nödstopp => stäng av 230V 300V
	${rv} =    Read S3
	#Log to Console    S3 is ${rv}
	Sleep    ${DELAY_02s}

Turn Off 24V and 5Ve
	Power Control  ${p_24V}  ${OFF}
	Power Control  ${p_5Ve}  ${OFF}

Turn ON AC230V and DC300V
	# R1, R2 kan styras ut 230V, 300V GPA0, GPA1

	Log to Console    DC300V is turned on
	Power Control  ${DC_300V}  ${ON}
	Log to Console    AC230V is turned on
	Power Control  ${AC_230V}  ${ON}

