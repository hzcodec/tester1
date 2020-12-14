# -------------------------------------------------------------
# AD4112
# -------------------------------------------------------------
# Register for AD4112
COMMS = 0x00  # Communication register. All access must start here. (W)
STATUS = 0x00  # Status information (R)
ADCMODE = 0x01
IFMODE = 0x02
DATA = 0x04  # The data register contains the ADC conversion result (R)
GPIOCON = 0x06
ID = 0x07
GAIN = 0x99 # fake number, just to be able to handle the dispatcher

CH0 = 0x10 # Channel control register (R/W)
CH1 = 0x11
CH2 = 0x12
CH3 = 0x13
CH4 = 0x14
CH5 = 0x15
CH6 = 0x16
CH7 = 0x17
CH8 = 0x18
CH9 = 0x19
CH10 = 0x1a
CH11 = 0x1b
CH12 = 0x1c
CH13 = 0x1d
CH14 = 0x1e
CH15 = 0x1f

SETUPCON0 = 0x20  # Setup configuration register (R/W)
SETUPCON1 = 0x21
SETUPCON2 = 0x22
SETUPCON3 = 0x23
SETUPCON4 = 0x24
SETUPCON5 = 0x25
SETUPCON6 = 0x26
SETUPCON7 = 0x27

OFFSET0 = 0x30
OFFSET1 = 0x31

GAIN0 = 0x38
GAIN1 = 0x39

# AD412 parameters
RD = 0x40 # read bit in COMMS register
VIN0 = 0
VIN1 = 1
VIN2 = 2
VIN3 = 3
VIN4 = 4
VIN5 = 5
VIN6 = 6
VIN7 = 7

VIN0_VINCOM = 0x010  # Channel register CH<n>, voltage input to voltage input common
VIN1_VINCOM = 0x030
VIN2_VINCOM = 0x050
VIN3_VINCOM = 0x070
VIN4_VINCOM = 0x090
VIN5_VINCOM = 0x0b0
VIN6_VINCOM = 0x0d0
VIN6_VINCOM = 0x0f0

GP_DATA0 = 0x40  # bit 6 in GPIOCON
GP_DATA1 = 0x80  # bit 7 in GPIOCON

INT_OFFSET = 4
INT_GAIN = 5
SYSTEM_OFFSET = 6
SYSTEM_GAIN = 7

# Channel register CH0-CH7, 0x10 - 0x1f
CH_EN = 0x8000
SETUP_SEL_0 = 0x0000
SETUP_SEL_1 = 0x1000
SETUP_SEL_2 = 0x2000
SETUP_SEL_3 = 0x3000
SETUP_SEL_4 = 0x4000
SETUP_SEL_5 = 0x5000
SETUP_SEL_6 = 0x6000
SETUP_SEL_7 = 0x7000

INPUT_VIN0 = 0x0010
INPUT_VIN1 = 0x0030
INPUT_VIN2 = 0x0050
INPUT_VIN3 = 0x0070
INPUT_VIN4 = 0x0090
INPUT_VIN5 = 0x00b0
INPUT_VIN6 = 0x00d0
INPUT_VIN7 = 0x00f0

INPUT_VIN0_VIN1 = 0x0001
INPUT_VIN1_VIN0 = 0x0020
INPUT_VIN2_VIN3 = 0x0043
INPUT_VIN3_VIN2 = 0x0062
INPUT_VIN4_VIN5 = 0x0085
INPUT_VIN5_VIN4 = 0x00a4
INPUT_VIN6_VIN7 = 0x00c7
INPUT_VIN7_VIN6 = 0x00e6

IIN3 = 0x018b
IIN2 = 0x01aa
IIN2 = 0x01aa
IIN1 = 0x01c9
IIN0 = 0x01e8

# ADC mode register ADCMODE, 0x01
REF_EN = 0x8000
SING_SYNC = 0x2000
CONT_CONV = 0x0000
SING_CONV = 0x0010

# Channel register IFMODE, 0x02
CONTREAD = 0x80
DATA_STAT = 0x40

# Configuration register, SETUPCON0-7
BI_POLAR = 0x1000
REF_BUFP = 0x0800
REF_BUFM = 0x0400
INBUF_EN = 0x0300
REF_SEL_INT = 0x0020

# ------------------------------------------------------------------
# help functions
# ------------------------------------------------------------------
def ad4112_get_adc_mode_name(inp):
	if inp == CONT_CONV:
		return 'CONT_CONV'
	elif inp == SING_CONV:
		return 'SING_CONV'
	else:
		return ERROR_MSG

setup_name = {
    SETUP_SEL_0: lambda: "SETUP_SEL_0",
    SETUP_SEL_1: lambda: "SETUP_SEL_1",
    SETUP_SEL_2: lambda: "SETUP_SEL_2",
    SETUP_SEL_3: lambda: "SETUP_SEL_3",
    SETUP_SEL_4: lambda: "SETUP_SEL_4",
    SETUP_SEL_5: lambda: "SETUP_SEL_5",
    SETUP_SEL_6: lambda: "SETUP_SEL_6",
    SETUP_SEL_7: lambda: "SETUP_SEL_7",
}

def ad4112_get_setup_name(inp):
	return setup_name[inp]()

input_name = {
    INPUT_VIN0: lambda: "INPUT_VIN0",
    INPUT_VIN1: lambda: "INPUT_VIN1",
    INPUT_VIN2: lambda: "INPUT_VIN2",
    INPUT_VIN3: lambda: "INPUT_VIN3",
    INPUT_VIN4: lambda: "INPUT_VIN4",
    INPUT_VIN5: lambda: "INPUT_VIN5",
    INPUT_VIN6: lambda: "INPUT_VIN6",
    INPUT_VIN7: lambda: "INPUT_VIN7",
    INPUT_VIN0_VIN1: lambda: "INPUT_VIN0_VIN1",
    INPUT_VIN1_VIN0: lambda: "INPUT_VIN1_VIN0",
    INPUT_VIN2_VIN3: lambda: "INPUT_VIN2_VIN3",
    INPUT_VIN3_VIN2: lambda: "INPUT_VIN3_VIN2",
    INPUT_VIN4_VIN5: lambda: "INPUT_VIN4_VIN5",
    INPUT_VIN5_VIN4: lambda: "INPUT_VIN5_VIN4",
    INPUT_VIN6_VIN7: lambda: "INPUT_VIN6_VIN7",
    INPUT_VIN7_VIN6: lambda: "INPUT_VIN7_VIN6",
    IIN0: lambda: "IIN0+,IIN0-",
    IIN1: lambda: "III1+,IIN1-",
    IIN2: lambda: "III2+,IIN2-",
    IIN3: lambda: "III3+,IIN3-",
}

def ad4112_get_input_name(inp):
	return input_name[inp]()

def ad4112_get_stat_name(inp):
	if inp == DATA_STAT:
		return 'DATA_STAT'
	else:
		return ERROR_MSG
