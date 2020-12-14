*** Settings ***
Library   Dialogs

Resource  220_04_062/common.robot
Resource  220_04_062/unicorn.robot
Resource  config_intec.robot

*** Variables ***
${CHECK_5V}    ${1}
${CHECK_12V}    ${2}
${CHECK_24V}    ${3}
${ISO_TEST_1}   ${4}
${ISO_TEST_2}   ${5}
${24VD_SENSE}   ${6}
${Red}     ${95}
${Green}   ${96}
${Yellow}  ${97}
${LED1}    ${98}
${LED2}    ${99}
${LED3}    ${100}
${LED4}    ${101}
${LED5}    ${102}
${LED6}    ${103}
${LED7}    ${104}
${LED8}    ${105}
${LED9}    ${106}
${LED10}   ${107}
${LED11}   ${108}
${LED12}   ${109}
${LED13}   ${110}
${LED14}   ${111}
${LED15}   ${112}
${LED16}   ${113}
${LED17}   ${114}
${LED18}   ${115}
${UNCHECK}    ${999}

*** Keywords ***
5V Incorrect
	[Arguments]  ${rv}
	Log to Console    *** 5V is either to low or high
	Should Be True  ${rv} > 4.5 and ${rv} < 5.3

12V Incorrect
	[Arguments]  ${rv}
	Log to Console    *** 12V is either to low or high
	Should Be True  ${rv} > 5.5 and ${rv} < 6.5

24V Incorrect
	[Arguments]  ${rv}
	Log to Console    *** 24V is either to low or high
	Should Be True  ${rv} > 7.5 and ${rv} < 8.5

Setup ADC CH3 for Voltage Check
	Config ADC   ${ADC_GET_ID_DEV_0}
	Config ADC   ${ADC_CH3_DEV_0}
	Config ADC   ${ADC_SETUP_DEV_0}
	Config ADC   ${ADC_MODE1_DEV_0}
	Config ADC   ${ADC_IFMODE_DEV_0}

#[TODO]: maybe remove, same as above
Setup ADC CH5 for Voltage Check
	Config ADC   ${ADC_GET_ID_DEV_0}
	Config ADC   ${ADC_CH5_DEV_0}
	Config ADC   ${ADC_SETUP_DEV_0}
	Config ADC   ${ADC_MODE1_DEV_0}
	Config ADC   ${ADC_IFMODE_DEV_0}

MUX_V2
	[Arguments]   ${arg4}    ${arg3}    ${arg2}    ${arg1}
	Set MCP port   ${DIO_20}    ${arg1}
	Set MCP port   ${DIO_21}    ${arg2}
	Set MCP port   ${DIO_22}    ${arg3}
	Set MCP port   ${DIO_23}    ${arg4}

Setup MUX_V2 for Voltage Check
	[Arguments]   ${arg}

	Run Keyword If    ${arg} == ${CHECK_5V}    Run Keyword    MUX_V2    ${HIGH}   ${LOW}    ${LOW}    ${HIGH}
	Run Keyword If    ${arg} == ${CHECK_12V}   Run Keyword    MUX_V2    ${HIGH}   ${LOW}    ${LOW}    ${LOW}
	Run Keyword If    ${arg} == ${CHECK_24V}   Run Keyword    MUX_V2    ${LOW}    ${HIGH}   ${HIGH}   ${HIGH}
	Run Keyword If    ${arg} == ${ISO_TEST_1}  Run Keyword    MUX_V2    ${LOW}    ${HIGH}   ${LOW}    ${HIGH}
	Run Keyword If    ${arg} == ${ISO_TEST_2}  Run Keyword    MUX_V2    ${LOW}    ${HIGH}   ${HIGH}   ${LOW}
	Run Keyword If    ${arg} == ${24VD_SENSE}  Run Keyword    MUX_V2    ${HIGH}   ${LOW}    ${HIGH}   ${LOW}

	Run Keyword If    ${arg} == ${LED1}        Run Keyword    MUX_V2    ${LOW}    ${LOW}    ${LOW}    ${LOW}
	Run Keyword If    ${arg} == ${LED2}        Run Keyword    MUX_V2    ${LOW}    ${LOW}    ${LOW}    ${HIGH}
	Run Keyword If    ${arg} == ${Red}         Run Keyword    MUX_V2    ${LOW}    ${LOW}    ${HIGH}   ${LOW}
	Run Keyword If    ${arg} == ${Green}       Run Keyword    MUX_V2    ${LOW}    ${LOW}    ${HIGH}   ${HIGH}
	Run Keyword If    ${arg} == ${Yellow}      Run Keyword    MUX_V2    ${LOW}    ${HIGH}   ${LOW}    ${LOW}

MUX_V1
	[Arguments]   ${arg1}    ${arg2}    ${arg3}    ${arg4}
	Set MCP port   ${DIO_16}    ${arg1}
	Set MCP port   ${DIO_17}    ${arg2}
	Set MCP port   ${DIO_18}    ${arg3}
	Set MCP port   ${DIO_19}    ${arg4}

Setup MUX_V1 for Voltage Check
	[Arguments]   ${arg}
	Run Keyword If    ${arg} == ${LED3}    Run Keyword   MUX_V1    ${HIGH}    ${HIGH}    ${HIGH}    ${HIGH}
	Run Keyword If    ${arg} == ${LED4}    Run Keyword   MUX_V1    ${HIGH}    ${LOW}     ${LOW}     ${LOW}
	Run Keyword If    ${arg} == ${LED5}    Run Keyword   MUX_V1    ${LOW}     ${HIGH}    ${LOW}     ${LOW}
	Run Keyword If    ${arg} == ${LED6}    Run Keyword   MUX_V1    ${HIGH}    ${HIGH}    ${LOW}     ${LOW}
	Run Keyword If    ${arg} == ${LED7}    Run Keyword   MUX_V1    ${LOW}     ${LOW}     ${HIGH}    ${LOW}
	Run Keyword If    ${arg} == ${LED8}    Run Keyword   MUX_V1    ${HIGH}    ${LOW}     ${HIGH}    ${LOW}
	Run Keyword If    ${arg} == ${LED9}    Run Keyword   MUX_V1    ${HIGH}    ${LOW}     ${HIGH}    ${LOW}
	Run Keyword If    ${arg} == ${LED10}    Run Keyword  MUX_V1    ${HIGH}    ${HIGH}    ${HIGH}    ${LOW}
	Run Keyword If    ${arg} == ${LED11}    Run Keyword  MUX_V1    ${LOW}     ${LOW}     ${LOW}     ${HIGH}
	Run Keyword If    ${arg} == ${LED12}    Run Keyword  MUX_V1    ${HIGH}    ${LOW}     ${LOW}     ${HIGH}
	Run Keyword If    ${arg} == ${LED13}    Run Keyword  MUX_V1    ${LOW}     ${HIGH}    ${LOW}     ${HIGH}
	Run Keyword If    ${arg} == ${LED14}    Run Keyword  MUX_V1    ${HIGH}    ${HIGH}    ${LOW}     ${HIGH}
	Run Keyword If    ${arg} == ${LED15}    Run Keyword  MUX_V1    ${LOW}     ${LOW}     ${HIGH}    ${HIGH}
	Run Keyword If    ${arg} == ${LED16}    Run Keyword  MUX_V1    ${HIGH}    ${LOW}     ${HIGH}    ${HIGH}
	Run Keyword If    ${arg} == ${LED17}    Run Keyword  MUX_V1    ${LOW}     ${HIGH}    ${HIGH}    ${HIGH}
	Run Keyword If    ${arg} == ${LED18}    Run Keyword  MUX_V1    ${HIGH}    ${LOW}     ${HIGH}    ${LOW}
