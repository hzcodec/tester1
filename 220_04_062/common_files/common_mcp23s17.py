# -------------------------------------------------------------
# MCP23S17
# -------------------------------------------------------------
SPI_IOCON = 0x0a
# Registers port A
SPI_IODIRA = 0x00
SPI_IOPOLA = 0x02
SPI_GPPUA = 0x0c
SPI_GPIOA = 0x12

# pin numbers
SPI_GPA0 = 0  #
SPI_GPA1 = 1  #
SPI_GPA2 = 2  #
SPI_GPA3 = 3  #
SPI_GPA4 = 4  #
SPI_GPA5 = 5  # DigOut1
SPI_GPA6 = 6  # DigOut2
SPI_GPA7 = 7  #
SPI_PORT_A = 0  # Used during read, all bits are read


# Registers port B
SPI_IODIRB = 0x01
SPI_IOPOLB = 0x03
SPI_GPPUB = 0x0d
SPI_GPIOB = 0x13
# pin numbers
SPI_GPB0 = 0  #
SPI_GPB1 = 1  #
SPI_GPB2 = 2  #
SPI_GPB3 = 3  #
SPI_GPB4 = 4  #
SPI_GPB5 = 5  #
SPI_GPB6 = 6  #
SPI_GPB7 = 7  #
SPI_PORT_B = 0  # Used during read, all bits are read

SPI_MAX_GPIO_PORT = 7

# fake number, just to be able to handle the dispatcher
SPI_READ_A = 0x100
SPI_READ_B = 0x101
SPI_GPB_C = 0x102
SPI_OPTO_A_IN = 0x103
SPI_OPTO_B_IN = 0x104
SPI_OPTO_B_OUT = 0x105
SPI_OPTO_B_OUT = 0x106
