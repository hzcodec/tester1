# -------------------------------------------------------------
# MCP23017
# -------------------------------------------------------------
# Registers port A
I2C_IODIRA = 0x00
I2C_IOPOLA = 0x02
I2C_GPIOA = 0x12
I2C_READ_PORT_A = 0x98  # dummy value
I2C_READ_PORT_B = 0x99  # dummy value

# pin numbers
I2C_GPA0 = 0  # DC300V
I2C_GPA1 = 1  # AC230V
I2C_GPA2 = 2  # PE
I2C_GPA3 = 3  # 24V
I2C_GPA4 = 4  # 5V
I2C_GPA5 = 5  # L1
I2C_GPA6 = 6  # S1
I2C_GPA7 = 7  # CLOSED

# Registers port B
I2C_IODIRB = 0x01
I2C_IOPOLB = 0x03
I2C_GPIOB = 0x13
# pin numbers
I2C_GPB0 = 0  # S3
I2C_GPB1 = 1  # A0
I2C_GPB2 = 2  # A1
I2C_GPB3 = 3  # A2
I2C_GPB4 = 4  # SW_RESET
I2C_GPB5 = 5  # READY
I2C_GPB6 = 6  # RESET
I2C_GPB7 = 7  # SAFE
