*** Settings ***

*** Variables ***

${DELAY_01s} =    0.1
${DELAY_02s} =    0.2
${DELAY_05s} =    0.5
${DELAY_1s} =    1.0
${DELAY_2s} =    2.0
${DELAY_3s} =    3.0

# input/output mode
${OUT} =   0
${IN} =    1

# port ON/OFF mode
${OFF} =   0
${ON} =    1

# level
${HIGH} =  1
${LOW} =  0

${DUMMY} =  0

# Relay index controlled by MCP23017 (addr=0)
${DC_300V} =  0
${AC_230V} =  1
${PROTECTED_EARTH} =  2
${p_24V} =  3
${p_5Ve} =  4
${L1} =  5

${S1} =     0
${S2} =     1
${READY} =  2
${SAFE} =   3
${RESET} =  4

# Relay names controlled by MCP23017 (addr=1)
${RELAY1} =    0
${RELAY2} =    1
${RELAY3} =    2
${RELAY4} =    3
${RELAY5} =    4
${RELAY6} =    5
${RELAY7} =    6
${RELAY8} =    7
${RELAY9} =    8
${RELAY10} =   9
${RELAY11} =   10
${RELAY12} =   11
${RELAY13} =   12
${RELAY14} =   13
${RELAY15} =   14
${RELAY16} =   15

# =======}======================================================================================
# MCP23017 device
# =============================================================================================
# Port 0 and 1 are configured during initialization (used as chip enable).
# Don't use them for your own purpose.
${SPARE0} =    0  # MCP23017, GPB0
${SPARE1} =    1  # MCP23017, GPB1


# These ports are avalilable for the user
${SPARE2} =    2  # MCP23017, GPB2
${SPARE3} =    3  #    -"-  , GPB3
${SPARE4} =    4  #    -"-  , GPB4
${SPARE5} =    5  #    -"-  , GPB5
${SPARE6} =    6  #    -"-  , GPB6
${SPARE7} =    7  #    -"-  , GPB7


# =============================================================================================
# MCP23s17 device
# =============================================================================================
${SPI_IOCON} =   0x0a

${SPI_IODIRA} =   0x00
${SPI_GPIOA} =   0x12
${SPI_GPPUA} =   0x0c
${SPI_GPA0} =    0
${SPI_GPA1} =    1
${SPI_GPA2} =    2
${SPI_GPA3} =    3
${SPI_GPA4} =    4
${SPI_GPA5} =    5
${SPI_GPA6} =    6
${SPI_GPA7} =    7

${SPI_IODIRB} =   0x01
${SPI_GPIOB} =   0x13
${SPI_GPPUB} =   0x0d
${SPI_GPB0} =    0
${SPI_GPB1} =    1
${SPI_GPB2} =    2
${SPI_GPB3} =    3
${SPI_GPB4} =    4
${SPI_GPB5} =    5
${SPI_GPB6} =    6
${SPI_GPB7} =    7

# fake number, just to be able to handle the dispatcher
${SPI_READ_A} =     0x100
${SPI_READ_B} =     0x101
${SPI_GPB_C} =         0x102
${SPI_OPTO_A_IN} =     0x103
${SPI_OPTO_B_IN} =     0x104
${SPI_OPTO_B_OUT} =    0x105
${SPI_OPTO_B_OUT} =    0x106


# =============================================================================================
# DAC61408 device
# =============================================================================================
# Registers
${DEVICE_ID} =    0x01
${DAC_STATUS} =    0x02
${DAC0} =    0x14
${DAC1} =    0x15
${DAC2} =    0x16
${DAC3} =    0x17
${DAC4} =    0x18
${DAC5} =    0x19
${DAC6} =    0x1a
${DAC7} =    0x1b

${DACRANGE0} =    0x0b  # DAC[7:4]
${DACRANGE1} =    0x0c  # DAC[3:0]

${RAMP} =   0x99

# DAC61408 parameters
${DAC_RANGE_0V_p5V} =    0x0  # 0 to 5V
${DAC_RANGE_0V_p10V} =    0x1  # 0 to 10V
${DAC_RANGE_0V_p20V} =    0x2  # 0 to 20V
${DAC_RANGE_m5V_p5V} =    0x9  # -5 to +5V
${DAC_RANGE_m10V_p10V} =    0xa  # -10 to +10V
${DAC_RANGE_m20V_p20V} =    0xc  # -20 to +20V
${DAC_RANGE_m2V5_p2V5} =    0xe  # -2.5 to +2.5V

# Output channel
${OUT_0} =   0
${OUT_1} =   1
${OUT_2} =   2
${OUT_3} =   3
${OUT_4} =   4
${OUT_5} =   5
${OUT_6} =   6
${OUT_7} =   7


# =============================================================================================
# AD4112 device
# =============================================================================================
# Register for AD4112
${COMMS} =    0x00  # Communication register. All access must start here. (W)
${STATUS} =    0x00  # Status information (R)
${ADCMODE} =    0x01
${IFMODE} =    0x02
${DATA} =    0x04  # The data register contains the ADC conversion result (R)
${GPIOCON} =    0x06
${ID} =    0x07
${GAIN} =    0x99  # fake number, just to be able to handle the dispatcher

${CH0} =   0x10   # Channel control register (R/W)
${CH1} =   0x11
${CH2} =   0x12
${CH3} =   0x13
${CH4} =   0x14
${CH5} =   0x15
${CH6} =   0x16
${CH7} =   0x17
${CH8} =   0x18
${CH9} =   0x19
${CH10} =   0x1a
${CH11} =   0x1b
${CH12} =   0x1c
${CH13} =   0x1d
${CH14} =   0x1e
${CH15} =   0x1f

${SETUPCON0} =   0x20  # Setup configuration register (R/W)
${SETUPCON1} =   0x21
${SETUPCON2} =   0x22
${SETUPCON3} =   0x23
${SETUPCON4} =   0x24
${SETUPCON5} =   0x25
${SETUPCON6} =   0x26
${SETUPCON7} =   0x27

${VIN_0} =   0
${VIN_1} =   1
${VIN_2} =   2
${VIN_3} =   3
${VIN_4} =   4
${VIN_5} =   5
${VIN_6} =   6
${VIN_7} =   7

${MEAS_CURR} =   0
${MEAS_VOLT} =   1
${MEAS_DIFF} =   2

${GP_DATA0} =   0x40  # bit 6 in GPIOCON
${GP_DATA1} =   0x80  # bit 7 in GPIOCON

${INT_OFFSET} =     4
${INT_GAIN} =       5
${SYSTEM_OFFSET} =  6
${SYSTEM_GAIN} =    7

# Channel register CH0-CH7, 0x10 - 0x1f
${CH_EN} =   0x8000
${SETUP_SEL_0} =   0x0000
${SETUP_SEL_1} =   0x1000
${SETUP_SEL_2} =   0x2000
${SETUP_SEL_3} =   0x3000
${SETUP_SEL_4} =   0x4000
${SETUP_SEL_5} =   0x5000
${SETUP_SEL_6} =   0x6000
${SETUP_SEL_7} =   0x7000

${INPUT_VIN0} =   0x0010
${INPUT_VIN1} =   0x0030
${INPUT_VIN2} =   0x0050
${INPUT_VIN3} =   0x0070
${INPUT_VIN4} =   0x0090
${INPUT_VIN5} =   0x00b0
${INPUT_VIN6} =   0x00d0
${INPUT_VIN7} =   0x00f0

${INPUT_VIN0_VIN1} =   0x0001
${INPUT_VIN1_VIN0} =   0x0020
${INPUT_VIN2_VIN3} =   0x0043
${INPUT_VIN3_VIN2} =   0x0062
${INPUT_VIN4_VIN5} =   0x0085
${INPUT_VIN5_VIN4} =   0x00a4
${INPUT_VIN6_VIN7} =   0x00c7
${INPUT_VIN7_VIN6} =   0x00e6
 
${IIN3} =   0x018b
${IIN2} =   0x01aa
${IIN2} =   0x01aa
${IIN1} =   0x01c9
${IIN0} =   0x01e8

# ADC mode register ADCMODE, 0x01
${REF_EN} =      0x8000
${SING_SYNC} =   0x2000
${CONT_CONV} =   0x0000
${SING_CONV} =   0x0010

# Channel register IFMODE, 0x02
${CONTREAD} =   0x80
${DATA_STAT} =  0x40

# Configuration register, SETUPCON0-7
${BI_POLAR} =      0x1000
${UNI_POLAR} =     0x0000
${REF_BUFP} =      0x0800
${REF_BUFM} =      0x0400
${INBUF_EN} =      0x0300
${REF_SEL_INT} =   0x0020

# =============================================================================================
# Device parameters
# =============================================================================================
${DAC61408_DEVICE} =    0
${AD4112_DEVICE_0} =    1
${AD4112_DEVICE_1} =    2
${MCP23S17_DEVICE_0} =    3
${MCP23S17_DEVICE_1} =    4

${MCP23S17_ADDR_0} =    0
${MCP23S17_ADDR_1} =    1

${NA} =    99  # Not Applicable. Can be changed for future use.

${SPI_ADDRESS_0} =    0
${SPI_ADDRESS_1} =    1

# =============================================================================================
# SPI MCP port declarations
# =============================================================================================
${DIO_0} =    0
${DIO_1} =    1
${DIO_2} =    2
${DIO_3} =    3
${DIO_4} =    4
${DIO_5} =    5
${DIO_6} =    6
${DIO_7} =    7

${DIO_8} =    8
${DIO_9} =    9
${DIO_10} =   10
${DIO_11} =   11
${DIO_12} =   12
${DIO_13} =   13
${DIO_14} =   14
${DIO_15} =   15

${DIO_16} =   16
${DIO_17} =   17
${DIO_18} =   18
${DIO_19} =   19
${DIO_20} =   20
${DIO_21} =   21
${DIO_22} =   22
${DIO_23} =   23

${GPB0_C} =   24
${GPB1_C} =   25
${GPB2_C} =   26
${GPB3_C} =   27
${GPB4_C} =   28
${GPB5_C} =   29
${GPB6_C} =   30
${GPB7_C} =   31

${SPI_GPIO_GPA0_A} =   32
${SPI_GPIO_GPA1_A} =   33
${SPI_GPIO_GPA2_A} =   34
${SPI_GPIO_GPA3_A} =   35
${SPI_GPIO_GPA4_A} =   36
${SPI_GPIO_GPA5_A} =   37
${SPI_GPIO_GPA6_A} =   38
${SPI_GPIO_GPA7_A} =   39

${SPI_GPIO_GPB0_A} =   40
${SPI_GPIO_GPB1_A} =   41
${SPI_GPIO_GPB2_A} =   42
${SPI_GPIO_GPB3_A} =   43
${SPI_GPIO_GPB4_A} =   44
${SPI_GPIO_GPB5_A} =   45
${SPI_GPIO_GPB6_A} =   46
${SPI_GPIO_GPB7_A} =   47

