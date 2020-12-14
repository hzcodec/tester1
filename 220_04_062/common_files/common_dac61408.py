# -------------------------------------------------------------
# DAC61408
# -------------------------------------------------------------
# Register for DAC61408
DAC0 = 0x14
DAC1 = 0x15
DAC2 = 0x16
DAC3 = 0x17
DAC4 = 0x18
DAC5 = 0x19
DAC6 = 0x1a
DAC7 = 0x1b
DEVICE_ID = 0x01
DAC_STATUS = 0x02
SPICONFIG = 0x03
GENCONFIG = 0x04
GPIOCON = 0x06
DACPWDWN = 0x09
DACRANGE0 = 0x0b  # DAC[7:4]
DACRANGE1 = 0x0c  # DAC[3:0]

RAMP = 0x99

# DAC61408 parameters
DAC_RANGE_0V_p5V = 0x0  # 0 to 5V
DAC_RANGE_0V_p10V = 0x1  # 0 to 10V
DAC_RANGE_0V_p20V = 0x2  # 0 to +20V
DAC_RANGE_m5V_p5V = 0x9  # -5 to +5V
DAC_RANGE_m10V_p10V = 0xa  # -10 to +10V
DAC_RANGE_m20V_p20V = 0xc  # -20 to +20V
DAC_RANGE_m2V5_p2V5 = 0xe  # -2.5 to +2.5V

DAC_OUT = 0x99 # fake number, just to be able to handle the dispatcher
